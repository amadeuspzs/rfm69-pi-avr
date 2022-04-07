known_senders = [ 2 ]

def processPacket(packet):
        """ Maps incoming packets to MQTT payloads

        Parameters:
                packet (packet): a single incoming packet

        Returns:
                (array (dict)): mapped topic:payload with rssi

	"""

        if packet.sender == 2:
                # ping
                topic = "radio/ping"
                state = packet.data[0]
                payload = state

        return [{ "topic": topic, "payload": payload}, {"topic": topic + "/rssi", "payload": packet.RSSI }]
