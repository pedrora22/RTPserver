import cv2
import socket
import struct
import time

VIDEO_PATH = "video.mp4"

DEST_IP = "127.0.0.1"
DEST_PORT = 5004

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(VIDEO_PATH)

sequence_number = 0
timestamp = 0
ssrc = 12345

FPS = 30
FRAME_DELAY = 1 / FPS

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Compacta em JPEG
    _, buffer = cv2.imencode(".jpg", frame)

    payload = buffer.tobytes()

    # RTP Header
    version = 2
    padding = 0
    extension = 0
    cc = 0

    marker = 0
    payload_type = 26

    first_byte = (
        (version << 6)
        | (padding << 5)
        | (extension << 4)
        | cc
    )

    second_byte = (
        (marker << 7)
        | payload_type
    )

    rtp_header = struct.pack(
        "!BBHII",
        first_byte,
        second_byte,
        sequence_number,
        timestamp,
        ssrc
    )

    packet = rtp_header + payload

    sock.sendto(packet, (DEST_IP, DEST_PORT))

    print(
        f"Frame={sequence_number} "
        f"Timestamp={timestamp}"
    )

    sequence_number += 1

    timestamp += 3000

    time.sleep(FRAME_DELAY)

cap.release()
sock.close()
