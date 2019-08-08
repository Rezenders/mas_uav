#!/usr/bin/env python2
import rospy
import jason_msgs.msg
import time
from threading import Event
from threading import Thread
from threading import RLock

my_name = 'scout'

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

def wait_droneB():
    while True:
        send_msg(0, 'rescuer1', 'askOne', 'online(X)')
        if "online" in messages and "\"rescuer1\"" in messages["online"]:
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

victims =    {1: (-27.604011, -48.518338),
            2: (-27.603716, -48.518078),
            3: (-27.603585, -48.518465),
            4: (-27.603693, -48.518641)}

def searchvictims():
    msgId = 1
    while True:
        if len(victims) == 0:
            break

        if 'global_pos' in perceptions:
            tol = 0.00001
            for v in victims.items():
                if(abs(float(perceptions['global_pos'][0]) - v[1][0]) < tol and float(perceptions['global_pos'][1]) - v[1][1] < tol):
                    print("Found Victm " + str(v) )
                    del victims[v[0]]
                    data = 'victim('+ str(v[0]) + ',' + str(v[1][0]) + ',' + str(v[1][1]) + ')'
                    send_msg(msgId,'rescuer1', 'tell', data)
                    msgId += 1
        time.sleep(0.5)

def fly():
    act("set_mode", ["GUIDED"])
    act("arm_motors", ["True"])

    takeOff(5)

    goToPos(-27.603683, -48.518052, 40);
    goToPos(-27.603518, -48.518329, 40);
    goToPos(-27.603677, -48.518652, 40);

    rtl()

if __name__ == '__main__':
    print("Starting python Agent node.")
    rospy.init_node('Agent')
    wait_droneB()

    thread_searchvictims = Thread(target = searchvictims)
    thread_searchvictims.start()
    fly()
    thread_searchvictims.join()
    raw_input()
