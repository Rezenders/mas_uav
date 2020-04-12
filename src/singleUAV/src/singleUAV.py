#!/usr/bin/env python2
import rospy
import jason_msgs.msg
import time
from pythonAgArch.pythonAgArch import *
import signal

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

def main():
    print("Starting python Agent node.")
    rospy.init_node('Agent', log_level=rospy.INFO)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    my_name = 'uav'
    agArch = AgArch(my_name)

    waitOnline(agArch)
    setModeGuided(agArch)
    armMotor(agArch)

    takeOff(agArch, 5)
    goToPos(agArch, -27.603683, -48.518052, 40)
    rtl(agArch)

if __name__ == '__main__':
    main()
