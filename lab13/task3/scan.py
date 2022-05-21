import netifaces
import netaddr
import scapy.all as scapy
import socket
from tkinter import *
from tkinter.ttk import Progressbar, Treeview
from sys import argv
from threading import Thread

INTERFACE = argv[1]

class MyWindow:
    def __init__(self, win):
        self.button_scan = Button(win, text='Сканировать', command=self.scan_start_thread)
        self.button_scan.place(x=10, y=10)

        self.pbar = Progressbar(win, orient='horizontal', mode='determinate', length=460)
        self.pbar.place(x=150, y=17)
        
        self.ips_tree = Treeview(win, column=("c1", "c2", "c3"), show="headings")
        self.ips_tree.place(x=10, y=50)
        self.ips_tree.column("# 1", anchor=CENTER)
        self.ips_tree.heading("# 1", text="IP")
        self.ips_tree.column("# 2", anchor=CENTER)
        self.ips_tree.heading("# 2", text="MAC")
        self.ips_tree.column("# 3", anchor=CENTER)
        self.ips_tree.heading("# 3", text="Hostname")

    def scan_start_thread(self):
        self.scan_thread = Thread(target=self.scan)
        self.scan_thread.start()

    def scan(self):
        self.pbar['value'] = 0
        self.ips_tree.delete(*self.ips_tree.get_children())

        ipinfo = netifaces.ifaddresses(INTERFACE)[netifaces.AF_INET][0]
        self.own_ip = ipinfo['addr']
        self.own_netmask = ipinfo['netmask']
        self.network_ip = netaddr.IPNetwork(f'{self.own_ip}/{self.own_netmask}')
        self.own_mac = netifaces.ifaddresses(INTERFACE)[netifaces.AF_LINK][0]['addr']
        self.own_name = socket.gethostname()

        all_net_hosts = list(self.network_ip)
        hosts_cnt = len(all_net_hosts)
        self.ips_tree.insert('', 'end', text='1', values=(self.own_ip, self.own_mac, self.own_name))
        for i, host in enumerate(all_net_hosts):
            self.pbar['value'] = round((i + 1) / hosts_cnt * 100)
            ip = str(host)
            packet = scapy.ARP(op='who-has', pdst=ip)
            reply = scapy.sr1(packet, timeout=0.01, verbose=False)
            if reply is None:
                continue
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except Exception:
                hostname = ''

            mac = reply.hwsrc
            self.ips_tree.insert('', 'end', text='1', values=(ip, mac, hostname))


window=Tk()
mywin=MyWindow(window)
window.title('Networks scanner')
window.geometry("625x250+10+10")
window.mainloop()