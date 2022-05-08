import socket
from sys import argv

if len(argv) != 3:
    print(f'Usage: {argv[0]} <host> <port>')

HOST = argv[1]
PORT = int(argv[2])

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

while True:
    msg = input('Enter message: ').encode('utf-8')

    sock.sendto(msg, (HOST, PORT))
    reply = sock.recv(1024).decode('utf-8')

    print('Got reply:', reply)
