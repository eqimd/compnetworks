#!/usr/bin/python3

import socket

from sys import argv
from io import StringIO

CRLF = '\r\n'

def main(host: str, port: int, filename: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    req = 'GET /' + filename + ' HTTP/1.0' + CRLF
    sock.sendall(req.encode('utf-8'))

    resp = sock.recv(1024).decode()
    buf = StringIO(resp)
    for _ in range(3):
        buf.readline()
    with open(filename, 'w') as f:
        f.write(buf.read())
    

if __name__ == '__main__':
    if len(argv) != 4:
        print('Usage: ./%s <host> <port> <filename>' % argv[0])
        exit(0)

    host = argv[1]
    port = int(argv[2])
    filename = argv[3]
    main(host, port, filename)