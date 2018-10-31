#!/usr/bin/env python2

import rospy
import mavros
import mavros_msgs.srv
import mavros_msgs.msg
import sensor_msgs.msg
import std_msgs.msg
# from mavros_msgs.msg import Waypoint, State

class FlightController:

    def __init__(self):
        self.state = mavros_msgs.msg.State()
        self.rel_alt = std_msgs.msg.Float64()
        self.global_pos = sensor_msgs.msg.NavSatFix()
        self.home_pos = mavros_msgs.msg.HomePosition()

    def set_mode(self, **kw):
        rospy.wait_for_service('/mavros/set_mode')
        try:
            set_mode_aux = rospy.ServiceProxy('/mavros/set_mode',
                                              mavros_msgs.srv.SetMode)
            set_mode_aux(**kw)
        except rospy.ServiceException as e:
            print("service set_mode call failed: %s." % e)

    def arm_motors(self, args, **kw):
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            arm_motors_aux = rospy.ServiceProxy('mavros/cmd/arming',
                                                mavros_msgs.srv.CommandBool)
            is_motors_armed = arm_motors_aux(args, **kw)
        except rospy.ServiceException as e:
            print("service arming call failed: %s." % e)

    def takeoff(self, **kw):
        rospy.wait_for_service('mavros/cmd/takeoff')
        try:
            takeoff_aux = rospy.ServiceProxy('mavros/cmd/takeoff',
                                             mavros_msgs.srv.CommandTOL)
            takeoff_aux(**kw)
        except rospy.ServiceException as e:
            print("service takeoff call failed: %s." % e)

    def land(self, **kw):
        rospy.wait_for_service('mavros/cmd/land')
        try:
            land_aux = rospy.ServiceProxy('mavros/cmd/land',
                                             mavros_msgs.srv.CommandTOL)
            land_aux(**kw)
        except rospy.ServiceException as e:
            print("service land call failed: %s." % e)

    def setpoint_global(self, **kw):
        setpoint_global_pub = rospy.Publisher(
            '/mavros/setpoint_position/global',
            mavros_msgs.msg.GlobalPositionTarget,
            queue_size=1,
            latch=True)

        header = std_msgs.msg.Header()
        header.stamp = rospy.Time.now()
        kw['header'] = header

        setpoint_global_pub.publish(**kw)

    # Execute mission
    def execute_mission(self, mission):
        if(mission.action == 'takeoff'):
            self.takeoff(**mission.params)
        elif(mission.action == 'setpoint'):
            self.setpoint_global(**mission.params)
        elif(mission.action == 'home'):
            self.set_mode(custom_mode='RTL')
        elif(mission.action == 'land'):
            self.land(**mission.params)

    # Drone State callback
    def state_callback(self, msg):
        self.state = msg

    # Drone rel_alt callback
    def rel_alt_callback(self, msg):
        self.rel_alt = msg

    # Drone global_pos callback
    def global_pos_callback(self, msg):
        self.global_pos = msg

    # Drone home_pos callback
    def home_pos_callback(self, msg):
        self.home_pos = msg


class action:
    def __init__(self):
        self.action = None
        self.params = dict()

    def __init__(self, action, **params):
        self.action = action
        self.params = params

# simulating syncronous agent (just for test)


def simulate_agent_node(ardupilot, mission):
    last_mission = action('')

    for m in mission:
        if(last_mission.action == 'takeoff'):
            while int(ardupilot.rel_alt.data) != last_mission.params['altitude']:
                pass

        elif(last_mission.action == 'setpoint'):
            while round(ardupilot.global_pos.latitude, 6) != round(last_mission.params['latitude'], 6) \
                and round(ardupilot.global_pos.longitude, 6) != round(last_mission.params['longitude'], 6):
                pass
        elif(last_mission.action == 'home'):
            while round(ardupilot.global_pos.latitude,6) != round(ardupilot.home_pos.latitude, 6) \
                and round(ardupilot.global_pos.longitude,6) != round(ardupilot.home_pos.longitude, 6):
                pass

        ardupilot.execute_mission(m)
        last_mission = m


def main():
    rospy.init_node('fly')

    # Rate Hz
    rate = rospy.Rate(2)

    ardupilot = FlightController()

    #TODO: encapsulate all subs in FlightController class
    state_sub = rospy.Subscriber('/mavros/state', mavros_msgs.msg.State,
                                 ardupilot.state_callback)

    rel_alt_sub = rospy.Subscriber(
        '/mavros/global_position/rel_alt',
        std_msgs.msg.Float64,
        ardupilot.rel_alt_callback)

    global_pos_sub = rospy.Subscriber(
        '/mavros/global_position/global',
        sensor_msgs.msg.NavSatFix,
        ardupilot.global_pos_callback)

    home_pos_sub = rospy.Subscriber(
        '/mavros/home_position/home',
        mavros_msgs.msg.HomePosition,
        ardupilot.home_pos_callback)

    while not ardupilot.state.mode == 'GUIDED':
        ardupilot.set_mode(custom_mode='GUIDED')
        rate.sleep()

    while not ardupilot.state.armed:
        ardupilot.arm_motors(True)
        rate.sleep()

    whole_mission = [
        action('takeoff', altitude=40),
        action(
            'setpoint',
            latitude= -27.603683,
            longitude= -48.518052,
            altitude=40),
        action(
            'setpoint',
            latitude= -27.603675,
            longitude= -48.518646,
            altitude=40),
        action('home'),
        action('land'),
    ]

    simulate_agent_node(ardupilot, whole_mission)

    rospy.spin()


if __name__ == '__main__':
    main()
