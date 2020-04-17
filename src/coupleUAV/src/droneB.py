#!/usr/bin/env python2
import rospy
import time
from pythonAgArch.pythonAgArch import *
import signal

from threading import Event
from threading import Thread
from threading import RLock

def wait_droneA(agArch):
    while True:
        agArch.send('droneA', 'askOne', 'online(X)')
        if "online" in agArch.messages and ["\"droneA\""] in agArch.messages["online"]:
            break
        else:
            agArch.message_event.wait(1.0)
            agArch.message_event.clear()


def goToPos(agArch, lat, long, alt):
    agArch.act("setpoint", [str(lat), str(long), str(alt)])
    tol = 0.00001
    while abs(float(agArch.perceptions['global_pos'][0]) - lat) > tol or abs(
            float(agArch.perceptions['global_pos'][1]) - long) > tol:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def takeOff(agArch, alt):
    agArch.act("takeoff", ["5"])
    while 'altitude' not in agArch.perceptions:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

    while abs(float(agArch.perceptions['altitude'][0]) - alt) > 0.1:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def rtl(agArch):
    agArch.act("set_mode", ["RTL"])
    tol = 0.00001
    while abs(float(agArch.perceptions['global_pos'][0]) - float(agArch.perceptions['home_pos'][0])) > tol or abs(
            float(agArch.perceptions['global_pos'][1]) - float(agArch.perceptions['home_pos'][1])) > tol or abs(float(agArch.perceptions['altitude'][0]) - 0) > 0.1:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def waitOnline(agArch):
    while 'state' not in agArch.perceptions:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

    while agArch.perceptions['state'][1] == 'False':
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def setModeGuided(agArch):
    while 'state' not in agArch.perceptions:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

    while agArch.perceptions['state'][0] != 'GUIDED':
        agArch.act("set_mode", ["GUIDED"])
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def armMotor(agArch):
    while 'state' not in agArch.perceptions:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

    while agArch.perceptions['state'][2] == 'False':
        agArch.act("arm_motors", ["True"])
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def deliverBuoys(agArch):
    while True:
        if "victim" in agArch.messages and len(agArch.messages["victim"]) > 0:
            agArch.message_lock.acquire()
            victim = agArch.messages["victim"].pop(0)
            agArch.message_lock.release()
            rescueVictm(agArch, float(victim[0]), float(victim[1]), float(victim[2]))
        else:
            agArch.message_event.wait(1000)

def rescueVictm(agArch, n, lat, long):
    waitOnline(agArch)
    setModeGuided(agArch)
    armMotor(agArch)

    takeOff(agArch, 5)

    goToPos(agArch, lat, long, 25);
    print("Droping buoy to victim" + "victim("+ str(n) + "," + str(lat) + "," +str(long)+")")
    rtl(agArch)
    print("Landed! beginning charging and buoy replacement!")
    time.sleep(3)

if __name__ == '__main__':
    print("Starting python Agent node.")
    rospy.init_node('python_agent', log_level=rospy.INFO)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    my_name = 'droneB'
    agArch = AgArch(my_name)

    wait_droneA(agArch)
    deliverBuoys(agArch)
