#!/usr/bin/env python2

import rospy
import std_msgs.msg
from flight_controller import FlightController, Action

jason_percepts_pub = rospy.Publisher(
    '/jason/percepts',
    std_msgs.msg.String,
    queue_size=1,
    latch=False)

def act(msg, ardupilot):
    mission = Action(msg, altitude=40)
    if(msg == 'takeoff' and int(ardupilot.rel_alt.data) == 40):
        jason_percepts_pub.publish("done(takeoff)")

    if(msg == 'takeoff'):
        ardupilot.execute_mission(mission)


def main():
    rospy.init_node('jason_flight')
    rate = rospy.Rate(1)

    ardupilot = FlightController()

    while not ardupilot.state.mode == 'GUIDED':
        ardupilot.set_mode(custom_mode='GUIDED')
        rate.sleep()

    while not ardupilot.state.armed:
        ardupilot.arm_motors(True)
        rate.sleep()

    jason_action_sub = rospy.Subscriber(
        '/jason/action',
        std_msgs.msg.String,
        act(ardupilot))

    rospy.spin()

if __name__ == '__main__':
    main()
