import socket
from sys import argv

if len(argv) != 3:
    print(f'Usage: {argv[0]} <host> <port>')

HOST = argv[1]
PORT = int(argv[2])

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))

while True:
    msg, addr = sock.recvfrom(1024)
    msg = msg.decode('utf-8')
    print('Got message:', msg)
    reply = msg.upper().encode('utf-8')
    sock.sendto(reply, addr)
