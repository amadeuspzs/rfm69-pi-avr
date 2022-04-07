from RFM69 import Radio, FREQ_433MHZ
from utils import *
import paho.mqtt.publish as publish
import time

# radio settings
node_id = 1
network_id = 1
# encryptKey = "sampleEncryptKey"
debug = False

# mqtt settings
hostname = "192.168.1.199"
port = 1883
client_id = "rfm69-pi"

print("Attaching to radio...")

# process incoming packets
# with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=True, encryptionKey=encryptKey) as radio:
with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=True, verbose=debug) as radio:
    while True:
        if radio.has_received_packet():
            for packet in radio.get_packets():
                if packet.sender in list(known_senders.keys()):
                    print(f"Processing {known_senders[packet.sender]}")
                    # extract mqtt payload from packet
                    data = processPacket(packet)
                    print("Publishing to MQTT...")
                    publish.multiple(
                        data,
                        hostname=hostname,
                        port=port,
                        client_id=client_id,
                        keepalive=60,
                        will=None,
                        auth=None,
                        tls=None,
                        transport="tcp",
                    )
                else:
                    print("Unknown sender: ", packet)
        time.sleep(1)  # seconds
