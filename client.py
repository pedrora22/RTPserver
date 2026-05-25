import socket
import cv2
import numpy as np

from rtp_packet import RTPPacket
from security import decrypt

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((HOST, PORT))

print("Cliente RTP aguardando pacotes...\n")
print("Pressione 'q' na janela do vídeo para sair.\n")

while True:
    data, addr = client_socket.recvfrom(65536)

    packet = RTPPacket.decode(data)

    frame_data = np.frombuffer(decrypt(packet['payload']), dtype=np.uint8)
    frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

    if frame is not None:
        cv2.imshow("RTP Video Stream", frame)
        print(f"Frame {packet['sequence']} recebido | ts={packet['timestamp']}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
cv2.destroyAllWindows()
