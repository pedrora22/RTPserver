import socket
import struct
import cv2
import numpy as np

PORT = 5004

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("0.0.0.0", PORT))

while True:

    packet, addr = sock.recvfrom(65535)

    header = packet[:12]
    payload = packet[12:]

    fields = struct.unpack("!BBHII", header)

    sequence_number = fields[2]
    timestamp = fields[3]

    print(
        f"Recebido Seq={sequence_number} "
        f"Timestamp={timestamp}"
    )

    jpg = np.frombuffer(payload, dtype=np.uint8)

    frame = cv2.imdecode(jpg, cv2.IMREAD_COLOR)

    if frame is not None:
        cv2.imshow("RTP Client", frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
