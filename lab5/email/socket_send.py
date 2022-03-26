import time
import ssl

from socket import *
from base64 import b64encode


from_addr = input('Your email: ')
passw = input('Your email password: ')
rec_addr = input('Enter receiver email: ')
subj = input('Enter subject: ')
body = input('Enter message text: ')

msg = f"\r\n {body}"
endmsg = "\r\n.\r\n"
mailserver = ("smtp.gmail.com", 587)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(mailserver)
recv = sock.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
    exit(1)
heloCommand = 'HELO Alice\r\n'
sock.send(heloCommand.encode())
recv = sock.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')
    exit(1)

starttls = "STARTTLS\r\n".encode()
sock.send(starttls)
recv = sock.recv(1024)

ssl_sock = ssl.wrap_socket(sock)

email_enc = b64encode(from_addr.encode())
passw_enc = b64encode(passw.encode())

authorizationcmd = "AUTH LOGIN\r\n"

ssl_sock.send(authorizationcmd.encode())
recv = ssl_sock.recv(1024)
print(recv)

ssl_sock.send(email_enc + "\r\n".encode())
recv = ssl_sock.recv(1024)
print(recv)

ssl_sock.send(passw_enc + "\r\n".encode())
recv = ssl_sock.recv(1024)
print(recv)

mailFrom = f"MAIL FROM: <{from_addr}>\r\n"
ssl_sock.send(mailFrom.encode())
recv = ssl_sock.recv(1024).decode()
print(recv)

rcptTo = f"RCPT TO: <{rec_addr}>\r\n"
ssl_sock.send(rcptTo.encode())
recv = ssl_sock.recv(1024).decode()
print(recv)

data = "DATA\r\n"
ssl_sock.send(data.encode())
recv = ssl_sock.recv(1024).decode()
print(recv)

ssl_sock.send(f"Subject: {subj}\n\n{msg}".encode())
ssl_sock.send(endmsg.encode())
recv = ssl_sock.recv(1024)

quit = "QUIT\r\n"
ssl_sock.send(quit.encode())
recv = ssl_sock.recv(1024).decode()
print(recv)
ssl_sock.close()