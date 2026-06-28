"""
Packet parsers for each known RFM69 node.

To add a new node:
1. Add the node ID and nickname to SENDERS in hub.py
2. Add a function parse_node_N(data, rssi) below
3. Register it in PARSERS at the bottom of this file

Each parser receives:
    data (bytes): raw packet payload
    rssi (int):   received signal strength in dBm

Each parser returns:
    list of (topic, payload, retain) tuples, or [] on error
"""

import logging
import struct
import math

log = logging.getLogger(__name__)


def parse_ping(data, rssi):
    """Node 2 — ping: single byte state."""
    return [
        ("radio/ping", data[0], True),
        ("radio/ping/rssi", rssi, True),
    ]


def parse_reservoir(data, rssi):
    """Node 3 — water reservoir: struct { float cm; float tempC; float adcRatio; bool heartbeat; }"""
    # 4 bytes for float + 4 for float + 4 for float + 1 for bool = 13 bytes on AVR
    if len(data) < 13:
        log.error(
            "Reservoir packet too short: %d bytes, raw: %s", len(data), data.hex()
        )
        return []

    try:
        # '<' = little-endian
        # 'f' = distance_cm (4 bytes)
        # 'f' = temperature_c (4 bytes)
        # 'f' = adcRatio (4 bytes)
        # '?' = heartbeat (1 byte)
        cm, temp_c, adc_ratio, heartbeat = struct.unpack("<ffff?", data[:13])

        # Always publish your connection metrics
        updates = [
            ("reservoir/heartbeat", heartbeat, True),
            ("reservoir/rssi", rssi, True),
            ("reservoir/adc_ratio", round(adc_ratio, 3), True),
        ]

        # Only append sensor metrics if they are valid numbers.
        # This prevents publishing 'nan' to MQTT, meaning Home Assistant
        # (or your database) simply retains the last known good measurement.
        if not math.isnan(cm):
            if cm < 30:
                log.info(f"Skipping low measurement {cm}")
            else:
                updates.append(("reservoir/level", round(cm, 1), True))

        if not math.isnan(temp_c):
            updates.append(("reservoir/temp", round(temp_c, 1), True))

        return updates

    except struct.error as e:
        log.error("Failed to unpack reservoir packet: %s | raw: %s", e, data.hex())
        return []


# ---------------------------------------------------------------------------
# Registry — maps sender ID to parser function
# ---------------------------------------------------------------------------

PARSERS = {
    2: parse_ping,
    3: parse_reservoir,
}


def parse_packet(packet):
    """Dispatch incoming packet to the appropriate parser.
    Returns list of (topic, payload, retain) tuples, or [] on error."""
    sender = packet.sender
    data = bytes(packet.data)
    rssi = packet.RSSI

    parser = PARSERS.get(sender)
    if parser is None:
        log.warning("Unknown sender %d, raw: %s", sender, data.hex())
        return []

    return parser(data, rssi)
