#!/usr/bin/env python3
"""
RFM69 to MQTT gateway.
Receives packets from RFM69 radio nodes and publishes to MQTT.

Usage:
    python3 gateway.py
    python3 gateway.py --log-file /var/log/rfm69-gateway.log
    python3 gateway.py --log-file /var/log/rfm69-gateway.log --log-level DEBUG
    python3 gateway.py --no-log-file   # stdout only
"""

import argparse
import logging
import signal
import struct
import sys
import time

import paho.mqtt.client as mqtt
from RFM69 import Radio, FREQ_433MHZ

# --- defaults ---
DEFAULT_LOG_FILE  = "/var/log/rfm69-gateway.log"
DEFAULT_LOG_LEVEL = "INFO"

# --- radio config ---
NODE_ID    = 1
NETWORK_ID = 1

# --- mqtt config ---
MQTT_HOST   = "192.168.1.199"
MQTT_PORT   = 1883
MQTT_CLIENT = "rfm69-gateway"

# --- known senders ---
SENDERS = {
    2: "ping",
    3: "reservoir",
}


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging(log_file, log_level):
    level = getattr(logging, log_level.upper(), logging.INFO)
    handlers = [logging.StreamHandler()]
    if log_file:
        try:
            handlers.append(logging.FileHandler(log_file))
        except OSError as e:
            # don't crash if log file isn't writable, just warn on stdout
            print(f"WARNING: cannot open log file {log_file}: {e}", file=sys.stderr)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        handlers=handlers,
    )
    return logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Smoketest
# ---------------------------------------------------------------------------

def smoketest_radio():
    """Try to initialise the radio briefly to confirm the hardware is present.
    Returns True if the radio responds, False otherwise."""
    log = logging.getLogger(__name__)
    log.info("Smoketest: checking RFM69 module...")
    try:
        with Radio(FREQ_433MHZ, NODE_ID, NETWORK_ID, isHighPower=True, verbose=False) as radio:
            # Read the version register (0x10) - RFM69 should return 0x24
            version = radio.spi.get_register(0x10)
            if version == 0x24:
                log.info("Smoketest: RFM69 responded correctly (version=0x%02X)", version)
                return True
            else:
                log.error(
                    "Smoketest: unexpected version register value 0x%02X "
                    "(expected 0x24) — wrong module or SPI wiring issue?", version
                )
                return False
    except Exception as e:
        log.error("Smoketest: failed to communicate with RFM69 module: %s", e)
        log.error("Check: SPI enabled (raspi-config), wiring, and that no other process is using the radio")
        return False


# ---------------------------------------------------------------------------
# Packet parsing
# ---------------------------------------------------------------------------

def parse_packet(packet):
    """Returns list of (topic, payload, retain) tuples, or empty list on error."""
    log    = logging.getLogger(__name__)
    sender = packet.sender
    rssi   = packet.RSSI
    data   = bytes(packet.data)

    try:
        if sender == 2:
            # ping node: single byte state
            state = data[0]
            return [
                ("radio/ping",      state, True),
                ("radio/ping/rssi", rssi,  True),
            ]

        elif sender == 3:
            # reservoir node: struct { float cm; float tempC; }
            if len(data) < 8:
                log.error("Reservoir packet too short: %d bytes, raw: %s", len(data), data.hex())
                return []
            cm, temp_c = struct.unpack("ff", data[:8])
            return [
                ("reservoir/level",      round(cm, 1),     True),
                ("reservoir/temp",       round(temp_c, 1), True),
                ("reservoir/level/rssi", rssi,             True),
            ]

    except struct.error as e:
        log.error("Failed to unpack packet from sender %d: %s | raw: %s", sender, e, data.hex())
        return []

    log.warning("Unknown sender %d, raw: %s", sender, data.hex())
    return []


# ---------------------------------------------------------------------------
# MQTT callbacks
# ---------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    log = logging.getLogger(__name__)
    if rc == 0:
        log.info("MQTT connected to %s:%s", MQTT_HOST, MQTT_PORT)
    else:
        log.error("MQTT connection failed, rc=%d", rc)

def on_disconnect(client, userdata, rc):
    log = logging.getLogger(__name__)
    if rc != 0:
        log.warning("MQTT unexpected disconnect rc=%d — will reconnect", rc)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="RFM69 to MQTT gateway")
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument(
        "--log-file",
        default=DEFAULT_LOG_FILE,
        metavar="PATH",
        help=f"Path to log file (default: {DEFAULT_LOG_FILE})",
    )
    log_group.add_argument(
        "--no-log-file",
        action="store_true",
        help="Log to stdout only, no file",
    )
    parser.add_argument(
        "--log-level",
        default=DEFAULT_LOG_LEVEL,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help=f"Log level (default: {DEFAULT_LOG_LEVEL})",
    )
    parser.add_argument(
        "--skip-smoketest",
        action="store_true",
        help="Skip the RFM69 hardware smoketest on startup",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    log_file = None if args.no_log_file else args.log_file
    log = setup_logging(log_file, args.log_level)

    log.info("RFM69 gateway starting")
    log.info("Log level: %s", args.log_level.upper())
    if log_file:
        log.info("Logging to %s", log_file)

    if not args.skip_smoketest:
        if not smoketest_radio():
            log.error("Smoketest failed — exiting. Use --skip-smoketest to bypass.")
            sys.exit(1)

    # MQTT setup
    mqttc = mqtt.Client(client_id=MQTT_CLIENT)
    mqttc.on_connect    = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    mqttc.loop_start()

    # graceful shutdown
    def shutdown(sig, frame):
        log.info("Shutdown signal received, cleaning up...")
        mqttc.loop_stop()
        mqttc.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    log.info("Attaching to radio...")
    with Radio(FREQ_433MHZ, NODE_ID, NETWORK_ID, isHighPower=True, verbose=False) as radio:
        log.info("Listening for packets")
        while True:
            if radio.has_received_packet():
                for packet in radio.get_packets():
                    sender_name = SENDERS.get(packet.sender, f"unknown({packet.sender})")
                    log.info("Packet from %s RSSI=%d", sender_name, packet.RSSI)
                    for topic, payload, retain in parse_packet(packet):
                        mqttc.publish(topic, payload, retain=retain)
                        log.debug("  -> %s = %s", topic, payload)
            time.sleep(0.1)


if __name__ == "__main__":
    main()