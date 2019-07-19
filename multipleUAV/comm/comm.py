import time
from simple_settings import settings
import simple_comms as comms
import rospy
import std_msgs.msg
import jason_msgs.msg

def send_msg(msg):
    comms.send([msg.data], settings.IP_SEND, settings.PORT)
    print("ENVIOU " + msg.data)

def main():
    print("Starting Communication node.")
    rospy.init_node('Communication')

    send_msg_sub = rospy.Subscriber(
        '/comm/send_msg',
        std_msgs.msg.String,
        send_msg)

    comm_message_pub = rospy.Publisher(
        '/comm/receive_msg',
        std_msgs.msg.String,
        queue_size=1,
        latch=False)

    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        m=comms.recieve(settings.IP_LISTEN, settings.PORT)
        if m[1][0]:
            print(m[0])
            comm_message_pub.publish(m[0])

        rate.sleep()
    rospy.spin()

if __name__ == '__main__':
    main()
