import time
from socket import *

def send(msg, ip, port):
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    for m in msg:
        data = m
        s.sendto(data, (ip, port))
        print("Sending:   " + data)
        time.sleep(1)
    s.close()


def recieve(ip, port):
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((ip, port))
    m = s.recvfrom(1024)
    s.close()
    return m
