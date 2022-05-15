import socket
import datetime
from time import time
from tkinter import *
from random import choice
from string import ascii_letters

class MyWindow:
    def __init__(self, win):
        self.label_ip = Label(win, text='Введите IP получателя')
        self.label_port = Label(win, text='Выберите порт для получения')
        self.label_packets = Label(win, text='Введите число пакетов')
        self.t_ip=Entry(bd=3)
        self.t_port=Entry()
        self.t_packets=Entry()
        self.button_get_packets = Button(win, text='Отправить', command=self.send_packets)

        self.label_ip.place(x=50, y=50)
        self.t_ip.place(x=300, y=50)

        self.label_port.place(x=50, y=100)
        self.t_port.place(x=300, y=100)

        self.label_packets.place(x=50, y=150)
        self.t_packets.place(x=300, y=150)

        self.button_get_packets.place(x=175, y=200)

    def send_packets(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.t_ip.get(), int(self.t_port.get())))
        sock.sendall(bytes(self.t_packets.get(), encoding='utf-8'))
        for i in range(int(self.t_packets.get())):
            cur_time = datetime.datetime.now()
            msg = str(cur_time) + ' '.join(choice(ascii_letters) for _ in range((1024 - len(str(cur_time)))))
            sock.sendall(msg.encode('utf-8'))
        sock.close()


window=Tk()
mywin=MyWindow(window)
window.title('Отправитель TCP')
window.geometry("500x250+10+10")
window.mainloop()