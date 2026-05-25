import socket
import time
import random
import cv2

from rtp_packet import RTPPacket
from security import encrypt

HOST = "127.0.0.1"
PORT = 5000
VIDEO_FILE = "Rick Astley - Never Gonna Give You Up [HQ] - AllKindsOfStuff (480p, h264, youtube).mp4"
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
JPEG_QUALITY = 60
PACKET_LOSS_RATE = 0.1

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(VIDEO_FILE)
if not cap.isOpened():
    print(f"Erro: não foi possível abrir o vídeo '{VIDEO_FILE}'")
    exit(1)

fps = cap.get(cv2.CAP_PROP_FPS) or 25
frame_interval = 1.0 / fps

sequence = 1

print("Servidor RTP iniciado...\n")

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
    payload = encrypt(buffer.tobytes())

    # SIMULAÇÃO DE PACKET LOSS
    if random.random() < PACKET_LOSS_RATE:
        print(f"Pacote {sequence} perdido na rede")
        print("-" * 30)
        sequence += 1
        continue

    packet = RTPPacket(sequence, payload)
    server_socket.sendto(packet.encode(), (HOST, PORT))

    print(f"Frame {sequence} enviado | {len(payload)} bytes | ts={packet.timestamp}")
    print("-" * 30)

    sequence += 1

    # SIMULAÇÃO DE JITTER
    jitter = random.uniform(0, 0.02)
    time.sleep(frame_interval + jitter)
