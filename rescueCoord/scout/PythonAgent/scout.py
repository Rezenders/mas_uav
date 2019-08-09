#!/usr/bin/env python2
import rospy
import time
from threading import Thread
from rosJason import *

my_name = 'scout'
drone_number = 2

rosj = RosJason(my_name)

def wait_drones():
    while True:
        rosj.broadcast('askOne', 'online(X)')
        print(rosj.messages)
        if "online" in rosj.messages and len(rosj.messages["online"])==drone_number:
            break
        else:
            rosj.message_event.clear()
            rosj.message_event.wait(2.0)


def goToPos(lat, long, alt):
    rosj.act("setpoint", [str(lat), str(long), str(alt)])
    tol = 0.00001
    while abs(float(rosj.perceptions['global_pos'][0]) - lat) > tol or abs(
            float(rosj.perceptions['global_pos'][1]) - long) > tol:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def takeOff(alt):
    rosj.act("takeoff", ["5"])
    while 'altitude' not in rosj.perceptions:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

    while abs(float(rosj.perceptions['altitude'][0]) - alt) > 0.1:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def rtl():
    rosj.act("set_mode", ["RTL"])
    tol = 0.00001
    while abs(float(rosj.perceptions['global_pos'][0]) - float(rosj.perceptions['home_pos'][0])) > tol or abs(
            float(rosj.perceptions['global_pos'][1]) - float(rosj.perceptions['home_pos'][1])) > tol or abs(float(rosj.perceptions['altitude'][0]) - 0) > 0.1:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

victims =    {1: (-27.604011, -48.518338),
            2: (-27.603716, -48.518078),
            3: (-27.603585, -48.518465),
            4: (-27.603693, -48.518641)}

def searchvictims():
    while True:
        if len(victims) == 0:
            break

        if 'global_pos' in rosj.perceptions:
            tol = 0.00001
            for v in victims.items():
                if(abs(float(rosj.perceptions['global_pos'][0]) - v[1][0]) < tol and float(rosj.perceptions['global_pos'][1]) - v[1][1] < tol):
                    print("Found Victm " + str(v) )
                    del victims[v[0]]
                    data = 'victim_in_need('+ str(v[0]) + ',' + str(v[1][0]) + ',' + str(v[1][1]) + ')'
                    rosj.broadcast('tell', data)
        time.sleep(0.5)

def fly():
    rosj.act("set_mode", ["GUIDED"])
    rosj.act("arm_motors", ["True"])

    takeOff(5)

    goToPos(-27.603683, -48.518052, 40);
    goToPos(-27.603518, -48.518329, 40);
    goToPos(-27.603677, -48.518652, 40);

    rtl()

if __name__ == '__main__':
    print("Starting python Agent node.")
    rospy.init_node('Agent')
    wait_drones()

    thread_searchvictims = Thread(target = searchvictims)
    thread_searchvictims.start()
    fly()
    thread_searchvictims.join()
    raw_input()
