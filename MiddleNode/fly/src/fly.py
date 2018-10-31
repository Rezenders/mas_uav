#!/usr/bin/env python2

import rospy
from flight_controller import FlightController

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
