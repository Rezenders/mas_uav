import time
from simple_settings import settings
import simple_comms as comms
import rospy
import std_msgs.msg
import jason_msgs.msg

# while True:
#     print("{}: Test.".format(time.ctime()))
#
#     # Until device found alert other drones of status:
#     comms.send(["Test sending"], IP, PORT)
#
#     # Wait and look again for a pixhawk
#     time.sleep(2)

def send_msg(msg):
    print('oi')
    pass
    # comms.send([msg.data], settings.IP_SEND, settings.PORT)

def main():
    print("Starting Communication node.")
    rospy.init_node('Communication')

    send_msg_sub = rospy.Subscriber(
        '/agent/send_msg',
        std_msgs.msg.String,
        send_msg)

    receive_msg_pub = rospy.Publisher(
    '/jason/percepts',
    jason_msgs.msg.Perception,
    queue_size=1,
    latch=False)

    rate = 2
    while not rospy.is_shutdown():
        print(settings.IP_LISTEN)
        m=comms.recieve(settings.IP_LISTEN, settings.PORT)
        if m[1][0]:
            perception = jason_msgs.msg.Perception()
            perception.perception_name = "message"
            perception.parameters = m[0]
            perception.update = False
            print(m[0])
            receive_msg_pub.publish(perception)

        rate.sleep()
    rospy.spin()

if __name__ == '__main__':
    main()
