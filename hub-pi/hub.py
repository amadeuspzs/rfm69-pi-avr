from RFM69 import Radio, FREQ_433MHZ
import paho.mqtt.publish as publish
import time

node_id = 1
network_id = 1
#encryptKey = "sampleEncryptKey"
debug = False
def processPacket(packet):
	print("Processing data")
	if packet.sender == 2:
		topic = "bantam/door"
		state = packet.data[0]
		payload = "Open" if state == 1 else "Closed" if state == 0 else "Undefined"

	return({ "topic": topic, "payload": payload})

#with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=True, encryptionKey=encryptKey) as radio:
with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=debug) as radio:
	while True:
		if(radio.has_received_packet()):
			for packet in radio.get_packets():
				data = processPacket(packet)
				print(packet.data)
				print(packet.RSSI)
				print("Publishing to MQTT...")
				publish.single(data["topic"], payload=data["payload"], qos=0, retain=True, hostname="192.168.1.199", port=1883, client_id="rfm69-pi", keepalive=60, will=None, auth=None, tls=None, transport="tcp")
		time.sleep(0.1) #seconds
