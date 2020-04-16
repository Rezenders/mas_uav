#!/usr/bin/env python2
import rospy
import jason_msgs.msg
import time
from rosJason import *
import signal

my_name = 'uav'
rosj = RosJason(my_name)

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

def waitOnline():
    while 'state' not in rosj.perceptions:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

    while rosj.perceptions['state'][1] == 'False':
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def setModeGuided():
    while 'state' not in rosj.perceptions:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

    while rosj.perceptions['state'][2] == 'False':
        rosj.act("set_mode", ["GUIDED"])
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def armMotor():
    while 'state' not in rosj.perceptions:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

    while rosj.perceptions['state'][3] == 'False':
        rosj.act("arm_motors", ["True"])
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def main():
    print("Starting python Agent node.")
    rospy.init_node('Agent')
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    waitOnline()
    setModeGuided()
    armMotor()

    takeOff(5)
    goToPos(-27.603683, -48.518052, 40)
    rtl()

if __name__ == '__main__':
    main()
