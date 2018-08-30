#!/usr/bin/env python2

import rospy
import mavros
from mavros_msgs.srv import SetMode, CommandBool, CommandTOL, WaypointPush
from mavros_msgs.msg import Waypoint

def set_mode(**kw):
    rospy.wait_for_service('/mavros/set_mode')
    set_mode_aux = rospy.ServiceProxy('/mavros/set_mode', SetMode)
    set_mode_aux(**kw)

def arm_motors(args, **kw):
    rospy.wait_for_service('mavros/cmd/arming')
    arm_motors_aux = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
    arm_motors_aux(args, **kw)

def takeoff(**kw):
    rospy.wait_for_service('mavros/cmd/takeoff')
    takeoff_aux = rospy.ServiceProxy('mavros/cmd/takeoff', CommandTOL)
    takeoff_aux(**kw)

if __name__ == '__main__':
    rospy.init_node('fly')

    set_mode(custom_mode='GUIDED')
    arm_motors(True)
    takeoff(altitude=40)


#    rospy.wait_for_service('mavros/mission/push')
#    waypoint_push = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)
#    waypoints = []
#    waypoints.append(Waypoint(command=16, frame=2, x_lat=-27.603683, y_long=-48.518052, z_alt=10))
#    print(waypoints)
#    waypoint_push(waypoints=waypoints)
#
#    rospy.wait_for_service('mavros/cmd/land')
#    land = rospy.ServiceProxy('mavros/cmd/land', CommandTOL)
#    land(altitude=0)
