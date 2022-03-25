import socket

from sys import argv


if len(argv) != 3:
    print(f'Usage: {argv[0]} <host> <port>')

HOST = argv[1]
PORT = int(argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
    udp_sock.sendto(b'Connect', (HOST, PORT))
    while True:
        tm = udp_sock.recvfrom(1024)[0]
        print(tm.decode('utf-8'))
