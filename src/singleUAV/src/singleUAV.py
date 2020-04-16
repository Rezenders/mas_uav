#!/usr/bin/env python2
import rospy
import jason_msgs.msg
import time
from rosJason import *
import signal

def goToPos(rosj, lat, long, alt):
    rosj.act("setpoint", [str(lat), str(long), str(alt)])
    tol = 0.00001
    while abs(float(rosj.perceptions['global_pos'][0]) - lat) > tol or abs(
            float(rosj.perceptions['global_pos'][1]) - long) > tol:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def takeOff(rosj, alt):
    rosj.act("takeoff", ["5"])
    while 'altitude' not in rosj.perceptions:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

    while abs(float(rosj.perceptions['altitude'][0]) - alt) > 0.1:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def rtl(rosj):
    rosj.act("set_mode", ["RTL"])
    tol = 0.00001
    while abs(float(rosj.perceptions['global_pos'][0]) - float(rosj.perceptions['home_pos'][0])) > tol or abs(
            float(rosj.perceptions['global_pos'][1]) - float(rosj.perceptions['home_pos'][1])) > tol or abs(float(rosj.perceptions['altitude'][0]) - 0) > 0.1:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def waitOnline(rosj):
    while 'state' not in rosj.perceptions:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

    while rosj.perceptions['state'][1] == 'False':
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def setModeGuided(rosj):
    while 'state' not in rosj.perceptions:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

    while rosj.perceptions['state'][0] != 'GUIDED':
        rosj.act("set_mode", ["GUIDED"])
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def armMotor(rosj):
    while 'state' not in rosj.perceptions:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

    while rosj.perceptions['state'][2] == 'False':
        rosj.act("arm_motors", ["True"])
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def main():
    print("Starting python Agent node.")
    rospy.init_node('Agent', log_level=rospy.INFO)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    my_name = 'uav'
    rosj = RosJason(my_name)

    waitOnline(rosj)
    setModeGuided(rosj)
    armMotor(rosj)

    takeOff(rosj, 5)
    goToPos(rosj, -27.603683, -48.518052, 40)
    rtl(rosj)

if __name__ == '__main__':
    main()
