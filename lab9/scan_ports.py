import sys
import socket

if len(sys.argv) != 4:
    print(f'Usage: {sys.argv[0]} <target> <port begin> <port end>')
    exit(1)

target = sys.argv[1]
port_begin, port_end = map(int, (sys.argv[2], sys.argv[3]))

try:
    print('Opened ports:')
    
    socket.setdefaulttimeout(0.1)
    for port in range(port_begin, port_end + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = s.connect_ex((target, port))
        if res == 0:
            print(port)
        s.close()
            
except socket.gaierror:
    print('Can not get the server.')
    exit(1)
except socket.error:
    exit(1)
    print('Can not get the server.')
