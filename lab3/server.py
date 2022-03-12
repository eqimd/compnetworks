#!/usr/bin/python3

import socket

from concurrent.futures import ThreadPoolExecutor
from sys import argv
from urllib.parse import parse_qs, urlencode
from io import StringIO

CRLF = '\r\n'


def contentType(s: str):
    if s.endswith('.htm') or s.endswith('.html'):
        return 'text/html'

    if s.endswith('.ram') or s.endswith('.ra'):
        return 'audio/x-pn-realaudio'
    
    return 'application/octet-stream'


def process_connection(conn: socket.socket):
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    req = conn.recv(1024).decode()
    # while True:
    #     chunk = conn.recv(1024)
    #     print(len(chunk))
    #     if len(chunk) == 0:
    #         break
    #     req += chunk.decode()

    reqLine = StringIO(req).readline()
    tokens = reqLine.split(' ')
    filename = tokens[1]

    if (filename != ''):
        filename = filename[1:]

    ret = ''

    try:
        file = open(filename, 'r')
        statusLine = 'HTTP/1.0 200 OK' + CRLF
        contentTypeLine = 'Content-Type: ' + contentType(filename) + CRLF

        ret = statusLine + contentTypeLine + CRLF + file.read()

    except FileNotFoundError:
        statusLine = 'HTTP/1.0 404 Not Found' + CRLF
        contentTypeLine = 'Content-Type: text/html' + CRLF
        entityBody = '<HTML>' + \
            '<HEAD><TITLE>Not Found</TITLE></HEAD>' + \
            '<BODY>Not Found</BODY></HTML>'

        ret = statusLine + contentTypeLine + CRLF + entityBody
    
    conn.sendall(ret.encode('utf-8'))
    conn.close()


def main(host: str, port: int, concurrency_level: int):
    executor = ThreadPoolExecutor(concurrency_level)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()

    while True:
        conn, addr = sock.accept()
        executor.submit(process_connection, (conn))




if __name__ == '__main__':
    if len(argv) != 4:
        print('Usage: ./%s <host> <port> <concurrency_level>' % argv[0])
        exit(0)

    host = argv[1]
    port = int(argv[2])
    concurrency_level = int(argv[3])
    main(host, port, concurrency_level)