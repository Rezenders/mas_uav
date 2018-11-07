#!/usr/bin/env python2

import rospy
import std_msgs.msg
from flight_controller import FlightController, Action

jason_percepts_pub = rospy.Publisher(
    '/jason/percepts',
    std_msgs.msg.String,
    queue_size=1,
    latch=False)

ardupilot = FlightController()

def act(msg):
    print(msg.data)
    while not ardupilot.state.mode == 'GUIDED':
        ardupilot.set_mode(custom_mode='GUIDED')
#        rate.sleep()

    while not ardupilot.state.armed:
        ardupilot.arm_motors(True)
#        rate.sleep()
    
    mission = Action(msg.data, altitude=40)
    if(msg.data == 'takeoff' and int(ardupilot.rel_alt.data) == 40):
        jason_percepts_pub.publish("done(takeoff)")

    if(msg.data == 'takeoff'):
        ardupilot.execute_mission(mission)


def main():
    rospy.init_node('jason_flight')
    rate = rospy.Rate(1)

    jason_action_sub = rospy.Subscriber(
        '/jason/actions',
        std_msgs.msg.String,
        act)

    rospy.spin()

if __name__ == '__main__':
    main()
