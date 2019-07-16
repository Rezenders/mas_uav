#!/usr/bin/env python2
import simple_comms as comms

IP = '192.168.0.48'
PORT =1024

for i in range(10):
    m=comms.recieve(IP, PORT)
    if m[1][0]:
        print(m[0])
