import time
import simple_comms as comms

IP = '192.168.0.48'
PORT = 1024

while True:
    print("{}: Test.".format(time.ctime()))

    # Until device found alert other drones of status:
    comms.send(["Test sending"], IP, PORT)

    # Wait and look again for a pixhawk
    time.sleep(2)
