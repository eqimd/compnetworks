import socket
import struct
import time

def calc_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += int.from_bytes(data[i:i + 2], 'little')

    while checksum & 65535 != checksum:
        checksum = (checksum >> 16) + (checksum & 65535)

    return 65535 ^ checksum


def send_ping(dest, sock, ttl, timeout, reqs):
    addr = None
    print(f'TTL: {ttl}')
    for _ in range(reqs):
        try:
            initial_header = struct.pack("bbHHh", 8, 0, 0, ttl, 1)
            checksum = calc_checksum(initial_header)
            header = struct.pack("bbHHh", 8, 0, checksum, ttl, 1)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            sock.sendto(header, (dest, 1))
            start_time = time.time()
            sock.settimeout(timeout)
            recv, temp = sock.recvfrom(1024)
            if recv is not None:
                payload = recv[20:]
                if calc_checksum(payload) != 0:
                    print('Checksum is wrong.')
                icmp = recv[20:28]
                type, code, checksum, pid, seq = struct.unpack('bbHHh', icmp)
                if pid == id and type != 0:
                    print('ICMP error.')
                diff = int((time.time() - start_time) * 1000.00)
                print(f'\t{diff}  ms')
            if temp is not None:
                addr = temp
        except socket.timeout:
            print('\tTimed out.')

    if addr is not None:
        hostname = ''
        try:
            gethost = socket.gethostbyaddr(addr[0])
            if len(gethost) > 0:
                hostname = gethost[0]
        except:
            hostname = ''
        print(f'{hostname}[{addr[0]}]')
        if addr[0] == dest:
            return True
    else:
        print('\ttimed out.')
        return False
    return False


def route(dest, reqs, timeout):
    try:
        addr = socket.gethostbyname(dest)
    except socket.gaierror:
        print('Invalid destination')
        return
    print(f'Traceroute to {addr}')
    for ttl in range(1, 64):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        if (send_ping(addr, sock, ttl, timeout, reqs)):
            sock.close()
            break
        sock.close()


if __name__ == '__main__':
    route('ya.ru', 5, 5)