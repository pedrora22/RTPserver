import socket
import time
import random

from rtp_packet import RTPPacket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sequence = 1

print("Servidor RTP iniciado...\n")

while True:

 
    # SIMULAÇÃO DE PACKET LOSS
   
    if random.random() < 0.3:
        print("Pacote perdido na rede")
        print("-" * 30)

        sequence += 1

        continue

    mensagem = f"Frame de vídeo {sequence}"

    packet = RTPPacket(sequence, mensagem)

    server_socket.sendto(
        packet.encode(),
        (HOST, PORT)
    )

    print("Pacote enviado:")
    print(f"Sequência: {sequence}")
    print(f"Timestamp: {packet.timestamp}")
    print("-" * 30)

    sequence += 1

    
    # SIMULAÇÃO DE JITTER
    
    jitter = random.uniform(0.1, 1.5)

    time.sleep(jitter)