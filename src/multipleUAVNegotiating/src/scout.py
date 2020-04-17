#!/usr/bin/env python2
import rospy
import time
from threading import Thread
from pythonAgArch.pythonAgArch import *
import signal

drone_number = 3

def wait_drones(agArch):
    while True:
        agArch.broadcast('askOne', 'online(X)')
        if "online" in agArch.messages and len(agArch.messages["online"])==drone_number:
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

victims =    {1: (-27.604011, -48.518338),
            2: (-27.603716, -48.518078),
            3: (-27.603585, -48.518465),
            4: (-27.603693, -48.518641)}

def searchvictims(agArch):
    while True:
        if len(victims) == 0:
            break

        if 'global_pos' in agArch.perceptions:
            tol = 0.00001
            for v in victims.items():
                if(abs(float(agArch.perceptions['global_pos'][0]) - v[1][0]) < tol and float(agArch.perceptions['global_pos'][1]) - v[1][1] < tol):
                    print("Found Victm " + str(v) )
                    del victims[v[0]]
                    data = 'victim_in_need('+ str(v[0]) + ',' + str(v[1][0]) + ',' + str(v[1][1]) + ')'
                    agArch.broadcast('tell', data)
        time.sleep(0.5)

def fly(agArch):
    waitOnline(agArch)
    setModeGuided(agArch)
    armMotor(agArch)

    takeOff(agArch, 5)

    goToPos(agArch, -27.603683, -48.518052, 40);
    goToPos(agArch, -27.603518, -48.518329, 40);
    goToPos(agArch, -27.603677, -48.518652, 40);

    rtl(agArch)

if __name__ == '__main__':
    print("Starting python Agent node.")
    rospy.init_node('python_agent', log_level=rospy.INFO)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    my_name = 'scout'
    agArch = AgArch(my_name)

    wait_drones(agArch)

    thread_searchvictims = Thread(target = searchvictims, kwargs={"agArch":agArch})
    thread_searchvictims.start()
    fly(agArch)
    thread_searchvictims.join()
    raw_input()
