import socket
from time import time
from tkinter import *

class MyWindow:
    def __init__(self, win):
        self.label_ip = Label(win, text='Введите IP')
        self.label_port = Label(win, text='Выберите порт для получения')
        self.label_speed = Label(win, text='Скорость передачи')
        self.label_packets = Label(win, text='Число полученных пакетов')
        self.t_ip=Entry(bd=3)
        self.t_port=Entry()
        self.t_speed=Entry()
        self.t_packets=Entry()
        self.button_get_packets = Button(win, text='Получить', command=self.get_packets)

        self.label_ip.place(x=50, y=50)
        self.t_ip.place(x=300, y=50)

        self.label_port.place(x=50, y=100)
        self.t_port.place(x=300, y=100)

        self.label_speed.place(x=50, y=150)
        self.t_speed.place(x=300, y=150)

        self.label_packets.place(x=50, y=200)
        self.t_packets.place(x=300, y=200)

        self.button_get_packets.place(x=175, y=250)

    def get_packets(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.t_ip.get(), int(self.t_port.get())))
        sock.listen(1)

        total_packets = 0
        packets_count = 0
        speed = 0
        first_time = 0
        last_time = 1
        addr, _ = sock.accept()
        total_packets = int(addr.recv(1024).decode('utf-8'))
        for _ in range(total_packets):
            try:
                cur_time = time()
                recv_msg = addr.recv(1024).decode('utf-8')
                if recv_msg != '':
                    packets_count += 1
                    if first_time == 0:
                        first_time = cur_time
            except socket.timeout:
                pass
        last_time = time()
        total_time = (last_time - first_time) * 1000
        if total_time > 0:
            speed = round(1024 * packets_count / total_time)

        self.t_speed.insert(END, f'{speed} kb/s')
        self.t_packets.insert(END, f'{packets_count} of {total_packets}')


window=Tk()
mywin=MyWindow(window)
window.title('Получатель TCP')
window.geometry("500x300+10+10")
window.mainloop()