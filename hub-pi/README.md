# rfm69-gateway

Receives packets from RFM69 radio nodes and publishes them to MQTT, intended for use with Home Assistant.

Built for a Raspberry Pi running DietPi with an RFM69 HAT at 433MHz.

## Hardware

- Raspberry Pi (any model with SPI header)
- RFM69HW/HCW HAT or breakout wired to SPI0
- SPI must be enabled via `dietpi-config` → Advanced Options → SPI

## Prerequisites

### System packages

```bash
sudo apt install python3 python3-venv python3-pip gcc python3-dev
```

### Log file

```bash
sudo touch /var/log/rfm69-gateway.log
sudo chown dietpi:dietpi /var/log/rfm69-gateway.log
```

### SPI permissions

```bash
sudo usermod -aG spi dietpi
```

## Installation

```bash
cd $HOME
git clone https://github.com/amadeuspzs/rfm69-pi-avr
cd /home/dietpi/rfm69-pi-avr/hub-pi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> **Why a venv?** `rpi-rfm69` depends on `RPi.GPIO` and `spidev` which can conflict with system packages on newer
> Debian/Ubuntu-based systems (including DietPi) that enforce PEP 668. A venv avoids this entirely and keeps
> dependencies isolated. It also means you can `pip install` without `sudo`.

## Configuration

Edit the constants at the top of `gateway.py`:

| Variable | Default | Description |
|---|---|---|
| `NODE_ID` | `1` | This gateway's radio node ID |
| `NETWORK_ID` | `1` | Must match all nodes on the network |
| `MQTT_HOST` | `192.168.1.199` | MQTT broker IP or hostname |
| `MQTT_PORT` | `1883` | MQTT broker port |
| `SENDERS` | `{2: "ping", 3: "reservoir"}` | Known node IDs and nicknames |

## Running

### Manual / testing

```bash
source venv/bin/activate

# default log file (/var/log/rfm69-gateway.log) + stdout
python3 gateway.py

# custom log file
python3 gateway.py --log-file /tmp/test.log

# stdout only, no file
python3 gateway.py --no-log-file

# verbose debug output
python3 gateway.py --log-level DEBUG

# skip hardware smoketest (e.g. if radio is known good)
python3 gateway.py --skip-smoketest
```

### As a systemd service

```bash
sudo cp rfm69-gateway.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rfm69-gateway
sudo systemctl start rfm69-gateway
```

Check status:

```bash
sudo systemctl status rfm69-gateway
journalctl -u rfm69-gateway -f
tail -f /var/log/rfm69-gateway.log
```

## Log rotation

```bash
sudo nano /etc/logrotate.d/rfm69-gateway
```

```
/var/log/rfm69-gateway.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
    postrotate
        systemctl restart rfm69-gateway
    endscript
}
```

## MQTT topics

| Topic | Value | Retained |
|---|---|---|
| `reservoir/level` | Distance in cm (float) | yes |
| `reservoir/temp` | Temperature in °C (float) | yes |
| `reservoir/level/rssi` | Signal strength in dBm | yes |
| `radio/ping` | Ping state byte | yes |
| `radio/ping/rssi` | Signal strength in dBm | yes |

## Radio payload structs

Payloads are packed C structs matching the Arduino node firmware.

**Node 3 — reservoir** (`sender == 3`):
```c
typedef struct {
  float cm;
  float tempC;
} Payload;
```

**Node 2 — ping** (`sender == 2`):
```c
uint8_t state;
```

## Smoketest

On startup the gateway reads the RFM69 version register over SPI. If the value is not `0x24` the process exits with an error rather than running silently with no radio. This catches SPI misconfiguration, wiring issues, and missing `dtoverlay=spi0-1cs` in `/boot/config.txt`.

To bypass: `--skip-smoketest`

## Adding a new node

1. Add the node ID and nickname to `SENDERS` in `gateway.py`
2. Add a new `elif sender == N:` block in `parse_packet()` matching the Arduino payload struct
3. Return a list of `(topic, payload, retain)` tuples