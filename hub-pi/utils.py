def processPacket(packet):
        """ Maps incoming packets to MQTT payloads

        Parameters:
                packet (packet): a single incoming packet

        Returns:
                (dict): mapped topic:payload

	"""

        if packet.sender == 2:
                # ping
                topic = "radio/ping"
                state = packet.data[0]
                payload = state

        return { "topic": topic, "payload": payload}
