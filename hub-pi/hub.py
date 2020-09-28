from RFM69 import Radio, FREQ_433MHZ
import datetime
import time

node_id = 1
network_id = 1

with Radio(FREQ_433MHZ, node_id, network_id, isHighPower=False, verbose=True, encryptionKey="sampleEncryptKey") as radio:
    print ("Starting loop...")
    
    rx_counter = 0
    tx_counter = 0

    while True:
        
        # Every 10 seconds get packets
        if rx_counter > 10:
            rx_counter = 0
            
            # Process packets
            for packet in radio.get_packets():
                print (packet)

        print("Listening...", len(radio.packets), radio.mode_name)
        delay = 0.5
        rx_counter += delay
        tx_counter += delay
        time.sleep(delay)
