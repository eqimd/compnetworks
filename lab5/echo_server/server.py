import socket

from sys import argv
from threading import Thread
from datetime import datetime
from time import sleep


if len(argv) != 3:
    print(f'Usage: {argv[0]} <host> <port>')

HOST = argv[1]
PORT = int(argv[2])

def listen_for_connections(sock, addrs):
    print('Waiting for connections...')
    while True:
        conn, addr = sock.recvfrom(1024)
        print(f'Connected: {addr}')
        addrs.append(addr)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
    udp_sock.bind((HOST, PORT))
    addrs = []
    listener = Thread(target=listen_for_connections, args=[udp_sock, addrs])
    listener.start()
    while True:
        sleep(1)
        tm = str(datetime.now())
        print(f'Current time: {tm}')
        for addr in addrs:
            print(f'Sending to {addr}...')
            udp_sock.sendto(tm.encode('utf-8'), addr)
