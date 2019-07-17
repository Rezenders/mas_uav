import time
from socket import *


def send(msg, broadcast_ip, port):
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    for m in msg:
        data = "{0}: Device: {1} Message:{2}".format(time.ctime(), gethostname(), m)
        s.sendto(data, (broadcast_ip, port))
        print("Sending " + data)
        time.sleep(1)
    s.close()


def recieve(broadcast_ip, port):
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((broadcast_ip, port))
    m = s.recvfrom(1024)
    s.close()
    return m
