import socket
from rtp_packet import RTPPacket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.bind((HOST, PORT))

print("Cliente RTP aguardando pacotes...\n")

while True:
    data, addr = client_socket.recvfrom(2048)

    packet = RTPPacket.decode(data)

    print("Pacote recebido:")
    print(f"Sequência: {packet['sequence']}")
    print(f"Timestamp: {packet['timestamp']}")
    print(f"Payload: {packet['payload']}")
    print("-" * 30)