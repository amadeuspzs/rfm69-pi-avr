[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python Version](https://img.shields.io/badge/Python-3.7.3-blue.svg)

# Raspberry Pi MQTT Hub

RFM69 <> Raspberry Pi <> MQTT Server

`hub.py` runs on your Raspberry Pi with attached RFM69 module, and proxies packets to your MQTT server.

## Installation

1. Setup a virtual environment e.g. `virtualenv hub`
2. Activate your virtual environment and install requirements: `pip install -r requirements.xtx`

## Configuration

1. Update payloads for your senders in `utils.py`


## Running

1. Run the hub with `python hub.py`
