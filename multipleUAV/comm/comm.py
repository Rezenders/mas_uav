from yellow_pages import *
from socket import *
import rospy
import std_msgs.msg
import jason_msgs.msg

def send_msg(msg):
    # data = "droneA, droneB, in_range(\"B\"), tell"
    data = msg.receiver + ", " + msg.sender + ", " + msg.data + ", " + msg.itlforce
    IP = agents_ip[msg.receiver][0]
    PORT = agents_ip[msg.receiver][1]

    s = socket(AF_INET, SOCK_DGRAM)
    s.sendto(data, (IP, PORT))
    s.close()
    print("Sending: " + data)

def main():
    print("Starting Communication node.")
    rospy.init_node('Communication')

    send_msg_sub = rospy.Subscriber(
        '/jason/send_msg',
        jason_msgs.msg.Message,
        send_msg)

    comm_message_pub = rospy.Publisher(
        '/jason/receive_msg',
        jason_msgs.msg.Message,
        queue_size=1,
        latch=False)

    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        IP = agents_ip["self"][0]
        PORT = agents_ip["self"][1]
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.bind((IP, PORT))
            m = s.recvfrom(1024)
            s.close()
            if m[1][0]:
                m_aux = [x.strip() for x in m[0].split(',')]
                message = jason_msgs.msg.Message()
                message.receiver = m_aux[0]
                message.sender = m_aux[1]
                message.data = m_aux[2]
                message.itlforce = m_aux[3]
                print(message)
                comm_message_pub.publish(message)
        except timeout:
            s.close()

        rate.sleep()
    rospy.spin()

if __name__ == '__main__':
    main()
