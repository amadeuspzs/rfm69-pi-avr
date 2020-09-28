from RFM69 import Radio, FREQ_433MHZ
import paho.mqtt.publish as publish
import datetime
import time

node_id = 1
network_id = 1
topic="bantam/door"

#encryptKey = "sampleEncryptKey"

#with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=True, encryptionKey=encryptKey) as radio:
with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=False) as radio:
    while True:
        # Process packets
        for packet in radio.get_packets():
	    if (packet.data[0] == 0):
		payload="Closed"
	    else:
		payload="Open"
            print(packet)
	    print(packet.data)
	    print(payload)
	    publish.single(topic, payload=payload, qos=0, retain=False, hostname="192.168.1.199", port=1883, client_id="rfm69-pi", keepalive=60, will=None, auth=None, tls=None, transport="tcp")
        time.sleep(1)
