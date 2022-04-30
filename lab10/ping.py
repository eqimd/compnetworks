import socket
import struct
import time
import random
import sys
from datetime import datetime
 
ICMP_ECHO_REQUEST = 8
 
BASE = 16
BASIC_BYTES = 2
MAX_BYTES = 2 ** BASE - 1
 
 
def calc_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += int.from_bytes(data[i:i + 2], 'little')

    while checksum & 65536 != checksum:
        checksum = (checksum >> 16) + (checksum & 65536)

    return 65536 ^ checksum
 
 
def receive_ping(sock, pid):
    time_rec = 0
    try:
        packet, addr = sock.recvfrom(1024)
        time_rec = time.time()
    except socket.timeout:
        return None
 
    cs_check = packet[20:]
    if calc_checksum(cs_check) != 0:
        print('Checksum is not valid')
        return None
    header = packet[20:28]
    type, code, checksum, mpid, seq = struct.unpack('bbHHh', header)
 
    if mpid == pid:
        double_bytes = struct.calcsize('d')
        return time_rec
 
 
def send_ping(sock, dest, pid):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, pid, 0)
    timestamp = str(datetime.now()).encode('utf-8')
    checksum = socket.htons(calc_checksum(header + timestamp))
 
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, checksum, pid, 1)
    packet = header + timestamp
    time_sent = time.time()
    while packet:
        sent = sock.sendto(packet, (dest, 1))
        packet = packet[sent:]
 
    return time_sent
 
 
def perform_ping(dest, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
 
    pid = int((id(timeout) * random.random()) % 65535)
    time_sent = send_ping(sock, dest, pid)
    sock.settimeout(timeout)
    time_rec = receive_ping(sock, pid)
 
    sock.close()
    if time_sent is None or time_rec is None:
        return None
    return time_rec - time_sent
 
 
def ping(host, timeout=1):
    dest = socket.gethostbyname(host)
    print('Pinging ' + dest + '...')
    while 1:
        delay = perform_ping(dest, timeout)
        if delay is not None:
            print('Got response in ' + str(round(delay * 1000, 3)) + ' ms')
        else:
            print('Timed out')
 
 
if __name__ == '__main__':
    ping(sys.argv[1], timeout=10)