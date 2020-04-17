import rospy
import jason_ros_msgs.msg
from threading import Event
from threading import RLock

class AgArch:
    def __init__(self, my_name):
        self.action_event = Event()
        self.perception_event = Event()
        self.perception_lock = RLock()
        self.message_event = Event()
        self.message_lock = RLock()
        self.perceptions = dict()
        self.messages = dict()
        self.msgId = 0
        self.my_name = my_name

        node_namespace = rospy.get_namespace()
        self.jason_actions_status_sub = rospy.Subscriber(
            node_namespace + 'jason/actions_status',
            jason_ros_msgs.msg.ActionStatus,
            self.action_status)

        self.jason_actions_pub = rospy.Publisher(
            node_namespace + 'jason/actions',
            jason_ros_msgs.msg.Action,
            queue_size=1,
            latch=False)

        self.jason_perceptions_sub = rospy.Subscriber(
            node_namespace + 'jason/percepts',
            jason_ros_msgs.msg.Perception,
            self.perception,
            queue_size=10
        )

        self.jason_send_msg_pub = rospy.Publisher(
            node_namespace + 'jason/send_msg',
            jason_ros_msgs.msg.Message,
            queue_size=1,
            latch=False)

        self.jason_receive_msg_sub = rospy.Subscriber(
            node_namespace + 'jason/receive_msg',
            jason_ros_msgs.msg.Message,
            self.receive_msg
        )

        rospy.set_param(rospy.get_namespace()+'jason/agent_name', self.my_name)

    def act(self, action_name, args):
        action = jason_ros_msgs.msg.Action()
        action.action_name = action_name
        action.parameters = args

        self.jason_actions_pub.publish(action)
        self.action_event.clear()
        self.action_event.wait()

    def action_status(self, msg):
        self.action_event.set()

    def perception(self, msg):
        self.perception_lock.acquire()
        self.perceptions[msg.perception_name] = msg.parameters
        self.perception_lock.release()
        self.perception_event.set()


    def send_msg(self, msgId, receiver, itlforce, msg):
        data = "<" + str(msgId)+','+self.my_name+","+itlforce+","+receiver+","+msg + ">"
        msg = jason_ros_msgs.msg.Message()
        msg.data = data
        self.jason_send_msg_pub.publish(msg)

    def send(self, receiver, itlforce, msg):
        self.send_msg(self.msgId, receiver, itlforce, msg)
        self.msgId += 1

    def broadcast(self, itlforce, msg):
        self.send_msg(self.msgId, "null", itlforce, msg)
        self.msgId += 1

    def replyTo(self, replyId, receiver, itlforce, msg):
        self.send_msg(str(self.msgId)+'->'+ str(replyId),receiver, itlforce, msg)

    def receive_msg(self, msg):
        msg_split = msg.data.strip('<>').split(',', 4)
        itlforce = msg_split[2]
        data = msg_split[-1]

        functor = data[:data.find('(')]
        args = data[(1+data.find('(')):data.find(')')]
        args = args.split(',')
        if itlforce == "tell":
            self.message_lock.acquire()
            if functor not in self.messages:
                self.messages[functor] = []
            if args not in self.messages[functor]:
                self.messages[functor].append(args)
            self.message_lock.release()
            self.message_event.set()

        if itlforce == "askOne":
            if functor == "online":
                d = "online(\"" + self.my_name + "\")"
                self.replyTo(msg_split[0], msg_split[1], 'tell', d)

        if itlforce == "untell":
            if functor == "victim_in_need":
                self.message_lock.acquire()
                if args in self.messages[functor]:
                    self.messages[functor].remove(args)
                self.message_lock.release()

def parseString(functor, *args):
    string = functor + "("
    for arg in args:
        for a in arg:
            string += str(a) + ","
    string = string.strip(",")
    string += ")"
    return string
