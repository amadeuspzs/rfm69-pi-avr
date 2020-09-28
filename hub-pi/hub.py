from RFM69 import Radio, FREQ_433MHZ
import datetime
import time

node_id = 1
network_id = 1
#encryptKey = "sampleEncryptKey"

#with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=True, encryptionKey=encryptKey) as radio:
with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=False) as radio:
    while True:
        # Process packets
        for packet in radio.get_packets():
            print (packet)
        time.sleep(1)
