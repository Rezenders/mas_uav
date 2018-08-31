#!/usr/bin/env python2

import rospy
import mavros
import mavros_msgs.srv
import mavros_msgs.msg
import std_msgs.msg
# from mavros_msgs.msg import Waypoint, State

class FlightController:

    def __init__(self):
        self.state = mavros_msgs.msg.State()
        self.rel_alt = std_msgs.msg.Float64()

    def set_mode(self, **kw):
        rospy.wait_for_service('/mavros/set_mode')
        try:
            set_mode_aux = rospy.ServiceProxy('/mavros/set_mode',
                mavros_msgs.srv.SetMode)
            set_mode_aux(**kw)
        except rospy.ServiceException, e:
           print ("service set_mode call failed: %s."%e)

    def arm_motors(self, args, **kw):
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            arm_motors_aux = rospy.ServiceProxy('mavros/cmd/arming',
                mavros_msgs.srv.CommandBool)
            is_motors_armed = arm_motors_aux(args, **kw)
        except rospy.ServiceException, e:
          print ("service arming call failed: %s."%e)

    def takeoff(self, **kw):
        rospy.wait_for_service('mavros/cmd/takeoff')
        try:
            takeoff_aux = rospy.ServiceProxy('mavros/cmd/takeoff',
                mavros_msgs.srv.CommandTOL)
            takeoff_aux(**kw)
        except rospy.ServiceException, e:
          print ("service takeoff call failed: %s."%e)

    def setpoint_global(self, **kw):
        setpoint_global_pub = rospy.Publisher('/mavros/setpoint_position/global',
            mavros_msgs.msg.GlobalPositionTarget, queue_size=1, latch=True)
        setpoint_global_pub.publish(**kw)

    #Execute mission
    def execute_mission(self, mission):
        if(mission.action=='takeoff'):
            self.takeoff(**mission.params)
        elif(mission.action=='setpoint'):
            self.setpoint_global(**mission.params)

    ## Drone State callback
    def state_callback(self, msg):
        self.state = msg

    ## Drone rel_alt callback
    def rel_alt_callback(self, msg):
        self.rel_alt = msg

class action:
    def __init__(self):
        self.action = None
        self.params = dict()

    def __init__(self, action, **params):
        print(action)
        print(params)
        self.action = action
        self.params = params

def main():
    rospy.init_node('fly')

    #Rate Hz
    rate = rospy.Rate(200)

    ardupilot = FlightController()

    state_sub = rospy.Subscriber('/mavros/state', mavros_msgs.msg.State,
        ardupilot.state_callback)

    rel_alt_sub = rospy.Subscriber('/mavros/global_position/rel_alt', std_msgs.msg.Float64,
        ardupilot.rel_alt_callback)

    while not ardupilot.state.mode == 'GUIDED':
        ardupilot.set_mode(custom_mode='GUIDED')
        rate.sleep()

    while not ardupilot.state.armed:
        ardupilot.arm_motors(True)
        rate.sleep()

    # whole_mission = [
    #     action('takeoff', altitude=40),
    #     action('setpoint', latitude=-27.603683, longitude=-48.518052),
    # ]
    #
    # ardupilot.execute_mission(whole_mission[1])

    ardupilot.setpoint_global(latitude=-27.603683, longitude=-48.518052)
    rospy.spin()

if __name__ == '__main__':
    main()
