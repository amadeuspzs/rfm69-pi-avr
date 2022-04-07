# senders are defined with integer values, enter your known senders below with a nickname for debugging
known_senders = {2: "ping"}


def processPacket(packet):
    """Maps incoming packets to MQTT payloads

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

    return [
        {"topic": topic, "payload": payload, "retain": True},
        {"topic": topic + "/rssi", "payload": packet.RSSI, "retain": True},
    ]
