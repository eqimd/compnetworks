import netifaces

for interf in netifaces.interfaces():
    print('Interface:', interf)
    info = netifaces.ifaddresses(interf)
    if netifaces.AF_INET in info.keys():
        print('\tIPv4 address:', info[netifaces.AF_INET][0]['addr'])
        print('\tNetmask:', info[netifaces.AF_INET][0]['netmask'])

    if netifaces.AF_INET6 in info.keys():
        print('\tIPv6 address:', info[netifaces.AF_INET6][0]['addr'])

