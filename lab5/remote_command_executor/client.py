import socket

from sys import argv

if len(argv) != 3:
    print(f'Usage: {argv[0]} <host> <port>')
    exit(0)

HOST = argv[1]
PORT = int(argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

command = input('Input command: ')
s.sendall(command.encode('utf-8'))
