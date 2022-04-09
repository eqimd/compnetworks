import socket

from sys import argv
from random import randint

if len(argv) != 3:
    print(f'Usage: {argv[0]} <host> <port>')

HOST = argv[1]
PORT = int(argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
    udp_sock.bind((HOST, PORT))
    while True:
        msg, addr = udp_sock.recvfrom(1024)

        r = randint(1, 5)
        if r == 5:
            continue

        msg = msg.decode('utf-8').upper().encode('utf-8')
        udp_sock.sendto(msg, addr)
