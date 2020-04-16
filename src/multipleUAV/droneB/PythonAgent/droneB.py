#!/usr/bin/env python2
import rospy
import jason_msgs.msg
import time
from threading import Event
from threading import Thread
from threading import RLock

my_name = 'droneB'

action_event = Event()
perception_event = Event()
message_event = Event()
message_lock = RLock()

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

def send_msg(msgId, receiver, itlforce, msg):
    data = "<" + str(msgId)+','+my_name+","+itlforce+","+receiver+","+msg + ">"
    msg = jason_msgs.msg.Message()
    msg.data = data
    jason_send_msg_pub.publish(msg)

messages = dict()

def receive_msg(msg):
    msg_split = msg.data.strip('<>').split(',', 4)
    itlforce = msg_split[2]
    data = msg_split[-1]

    functor = data[:data.find('(')]
    args = data[(1+data.find('(')):data.find(')')]
    if itlforce == "tell":
        message_lock.acquire()
        if functor not in messages:
            messages[functor] = []
        if args not in messages[functor]:
            messages[functor].append(args)
        message_lock.release()
        message_event.set()

    if itlforce == "askOne":
        if functor == "online":
            d = "online(\"" + my_name + "\")"
            send_msg(msg_split[0]+'->'+msg_split[0], msg_split[1], 'tell', d)

def wait_droneA():
    while True:
        send_msg(0, 'droneA', 'askOne', 'online(X)')
        if "online" in messages and "\"droneA\"" in messages["online"]:
            break
        else:
            message_event.clear()
            message_event.wait(1.0)


def goToPos(lat, long, alt):
    act("setpoint", [str(lat), str(long), str(alt)])
    tol = 0.00001
    while abs(float(perceptions['global_pos'][0]) - lat) > tol or abs(
            float(perceptions['global_pos'][1]) - long) > tol:
        perception_event.clear()
        perception_event.wait()

def takeOff(alt):
    act("takeoff", ["5"])
    while 'altitude' not in perceptions:
        perception_event.clear()
        perception_event.wait()

    while abs(float(perceptions['altitude'][0]) - alt) > 0.1:
        perception_event.clear()
        perception_event.wait()

def rtl():
    act("set_mode", ["RTL"])
    tol = 0.00001
    while abs(float(perceptions['global_pos'][0]) - float(perceptions['home_pos'][0])) > tol or abs(
            float(perceptions['global_pos'][1]) - float(perceptions['home_pos'][1])) > tol or abs(float(perceptions['altitude'][0]) - 0) > 0.1:
        perception_event.clear()
        perception_event.wait()


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

jason_send_msg_pub = rospy.Publisher(
    '/jason/send_msg',
    jason_msgs.msg.Message,
    queue_size=1,
    latch=False)

jason_receive_msg_sub = rospy.Subscriber(
    '/jason/receive_msg',
    jason_msgs.msg.Message,
    receive_msg
)

def deliverBuoys():
    while True:
        if "victim" in messages and len(messages["victim"]) > 0:
            message_lock.acquire()
            victim = messages["victim"].pop(0)
            message_lock.release()
            victim = victim.split(',')
            rescueVictm(float(victim[0]), float(victim[1]), float(victim[2]))
        else:
            message_event.wait(1000)

def rescueVictm(n, lat, long):

    act("set_mode", ["GUIDED"])
    act("arm_motors", ["True"])

    takeOff(5)
    goToPos(lat, long, 25);
    print("Droping buoy to victim" + "victim("+ str(n) + "," + str(lat) + "," +str(long)+")")
    rtl()
    print("Landed! beginning charging and buoy replacement!")
    time.sleep(3)

if __name__ == '__main__':
    print("Starting python Agent node.")
    rospy.init_node('Agent')

    wait_droneA()
    deliverBuoys()
