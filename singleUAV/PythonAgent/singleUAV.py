#!/usr/bin/env python2
import rospy
import jason_msgs.msg
import time
from threading import Event

action_event = Event()
perception_event = Event()


def act(action_name, args):
    action = jason_msgs.msg.Action()
    action.action_name = action_name
    action.parameters = args

    jason_actions_pub.publish(action)
    action_event.clear()
    action_event.wait()


def action_status(msg):
    action_event.set()


perceptions = dict()
def perception(msg):
    perceptions[msg.perception_name] = msg.parameters
    perception_event.set()


jason_actions_status_sub = rospy.Subscriber(
    '/jason/actions_status',
    jason_msgs.msg.ActionStatus,
    action_status)

jason_actions_pub = rospy.Publisher(
    '/jason/actions',
    jason_msgs.msg.Action,
    queue_size=1,
    latch=False)

jason_perceptions_sub = rospy.Subscriber(
    '/jason/percepts',
    jason_msgs.msg.Perception,
    perception
)


def main():
    print("Starting python Agent node.")
    rospy.init_node('Agent')
    tol = 0.00001

    act("set_mode", ["GUIDED"])
    act("arm_motors", ["True"])

    act("takeoff", ["5"])
    while 'altitude' not in perceptions:
        perception_event.clear()
        perception_event.wait()

    while abs(float(perceptions['altitude'][0]) - 5.0) > 0.1:
        perception_event.clear()
        perception_event.wait()

    act("setpoint", ["-27.603683", "-48.518052", "40"])
    while abs(float(perceptions['global_pos'][0]) - (-27.603683)) > tol and abs(
            float(perceptions['global_pos'][1]) - (-48.51805)) > tol:
        perception_event.clear()
        perception_event.wait()

    act("set_mode", ["RTL"])

if __name__ == '__main__':
    main()
