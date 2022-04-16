import socket

from sys import argv
from random import randint


IS_SERVER = True if input('Is it a server? (y/n): ') == 'y' else False
HOST = input('Enter host: ')
PORT = int(input('Enter port: '))
TIMEOUT_SECONDS = int(input('Enter timeout in seconds: '))

FILEPATH = ''
GET_OR_RECV = ''

if not IS_SERVER:
    FILEPATH = input('Enter filename: ')
    GET_OR_RECV = input('Get or send file? (get/send): ')


ACK_NO = 0
PACKETS = []

def get_new_recv(sock):
    global PACKETS
    global ACK_NO
    while True:
        try:
            packet, addr = sock.recvfrom(1024)
            if len(PACKETS) != 0 and packet == PACKETS[-1]:
                print('Got same packet, resending ACK.')
                send_bytes(sock,  addr, str(ACK_NO ^ 1).encode('utf-8'), add_ACK=False, wait_for_ack=False)
                continue
            else:
                print(f'Got packet with ACK {ACK_NO}')
                PACKETS.append(packet)
                send_bytes(sock,  addr, str(ACK_NO).encode('utf-8'), add_ACK=False, wait_for_ack=False)
                print(f'Sent ACK {ACK_NO}')
                ACK_NO ^= 1
                print(f'Set new ACK: {ACK_NO}')

            return (packet, addr)
        except socket.timeout:
            continue

def send_bytes(sock, addr, bytes, wait_for_ack=True, add_ACK=True):
    global ACK_NO
    if add_ACK:
        bytes = f'ACK{str(ACK_NO)}'.encode('utf-8') + bytes

    r = randint(1, 10)
    if r > 3:
        print('Sent packet:', bytes.decode('utf-8'))
        sock.sendto(bytes, addr)
    else:
        print('...imitating packet lost...')

    if wait_for_ack:
        while True:
            try:
                packet, addr = sock.recvfrom(1024)
            except socket.timeout:
                print('Did not get ACK, resending packet.')
                sock.sendto(bytes, addr)
                continue

            if packet.decode('utf-8') == str(ACK_NO):
                print(f'Got packet with ACK {ACK_NO}')
                ACK_NO ^= 1
                break

def get_file(sock, addr=None):
    print(f'Filename: {FILEPATH}')
    packet, addr = get_new_recv(sock)
    with open(FILEPATH, 'wb') as f:
        while packet.decode('utf-8')[4:] != 'END_OF_FILE':
            f.write(packet[4:])
            packet, addr = get_new_recv(sock)
        
        f.close()

def send_file(sock, addr):
    global FILEPATH
    with open(FILEPATH, 'rb') as f:
        while True:
            rd = f.read(1000)
            if rd.decode('utf-8') == '':
                send_bytes(sock, addr, 'END_OF_FILE'.encode('utf-8'), True)
                print('Ended sending file.')
                break

            send_bytes(sock, addr, rd, True)

        f.close()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
    udp_sock.settimeout(TIMEOUT_SECONDS)
    
    if IS_SERVER:
        udp_sock.bind((HOST, PORT))

        while True:
            print('Waiting for a command...')
            comm, addr = get_new_recv(udp_sock)
            print(f'Got a command: {comm.decode("utf-8")[4:]}')
            fn_bytes, addr = get_new_recv(udp_sock)
            FILEPATH = fn_bytes.decode('utf-8')[4:]
            if comm.decode('utf-8')[4:] == 'get':
                send_file(udp_sock, addr)
            else:
                get_file(udp_sock)
    else:
        send_bytes(udp_sock, (HOST, PORT), GET_OR_RECV.encode('utf-8'))
        send_bytes(udp_sock, (HOST, PORT), FILEPATH.encode('utf-8'))
        if GET_OR_RECV == 'get':
            get_file(udp_sock)
        else:
            send_file(udp_sock, (HOST, PORT))

