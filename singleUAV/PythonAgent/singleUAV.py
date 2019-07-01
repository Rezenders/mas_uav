#!/usr/bin/env python2
import rospy
import jason_msgs.msg
import time

jason_actions_pub = rospy.Publisher(
'/jason/actions',
jason_msgs.msg.Action,
queue_size=1,
latch=False)

def act(action_name, args):
    action = jason_msgs.msg.Action()
    action.action_name = action_name
    action.parameters = args

    jason_actions_pub.publish(action)

def main():
    print("Starting python Agent node.")
    rospy.init_node('Agent')

    act("set_mode",["GUIDED"])
    act("arm_motors",["True"])
    act("takeoff",["5"])
    time.sleep(10)
    act("setpoint",["-27.603683","-48.518052","40"])
    time.sleep(10)
    act("set_mode",["RTL"])
    time.sleep(1)
    act("land",[])

if __name__ == '__main__':
    main()
