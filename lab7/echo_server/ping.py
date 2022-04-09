import socket

from sys import argv
from datetime import datetime
from time import time

TIMEOUT_SECONDS = 1

if len(argv) != 3:
    print(f'Usage: {argv[0]} <host> <port>')

HOST = argv[1]
PORT = int(argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
    udp_sock.settimeout(TIMEOUT_SECONDS)
    for i in range(1, 11):
        msg = f'Ping {i} {datetime.now()}'

        starttime = time()
        udp_sock.sendto(msg.encode('utf-8'), (HOST, PORT))
        try:
            ans = udp_sock.recvfrom(1024)[0].decode('utf-8')
            rtt = time() - starttime
            print(ans, 'rtt =', rtt, 'seconds')
        except socket.timeout:
            print('Request timed out')
            continue
