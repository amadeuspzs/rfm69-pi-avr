from RFM69 import Radio, FREQ_433MHZ
import paho.mqtt.publish as publish
import datetime
import time

node_id = 1
network_id = 1
topic="bantam/door"
#encryptKey = "sampleEncryptKey"

def processPacket(packet):
	if packet.sender == 2:
		topic = "bantam/door"
		payload = "Open" if packet.data == 0 else "Closed"

	return({ "topic": topic, "payload": payload})

#with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=True, encryptionKey=encryptKey) as radio:
with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=False) as radio:
	while True:
		# Process packets
		for packet in radio.get_packets():
			data = processPacket(packet)
			publish.single(data["topic"], payload=data["payload"], qos=0, retain=False, hostname="192.168.1.199", port=1883, client_id="rfm69-pi", keepalive=60, will=None, auth=None, tls=None, transport="tcp")
			time.sleep(1)
