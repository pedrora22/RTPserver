import struct
import time

class RTPPacket:
    def __init__(self, sequence, payload):
        self.version = 2
        self.payload_type = 96
        self.sequence = sequence
        self.timestamp = int(time.time())
        self.ssrc = 12345
        self.payload = payload.encode()

    def encode(self):
        header = struct.pack(
            "!BBHII",
            0x80,
            self.payload_type,
            self.sequence,
            self.timestamp,
            self.ssrc
        )

        return header + self.payload

    @staticmethod
    def decode(packet):
        header = packet[:12]
        payload = packet[12:]

        fields = struct.unpack("!BBHII", header)

        return {
            "sequence": fields[2],
            "timestamp": fields[3],
            "payload": payload.decode()
        }