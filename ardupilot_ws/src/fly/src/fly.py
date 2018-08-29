#!/usr/bin/env python2

import rospy
import mavros
from mavros_msgs.srv import SetMode

if __name__ == '__main__':
    rospy.init_node('fly')

    rospy.wait_for_service('/mavros/set_mode')
    set_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
    set_mode(custom_mode='GUIDED')

