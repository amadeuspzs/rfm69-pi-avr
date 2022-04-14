import struct

# senders are defined with integer values, enter your known senders below with a nickname for debugging
known_senders = {2: "ping", 3: "reservoir"}


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
    elif packet.sender == 3:
        # water reservoir
        topic = "reservoir/level"
        distance = struct.unpack("f",bytes(packet.data))[0]
        payload = distance

    return [
        {"topic": topic, "payload": payload, "retain": True},
        {"topic": topic + "/rssi", "payload": packet.RSSI, "retain": True},
    ]
