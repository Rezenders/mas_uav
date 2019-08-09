#!/usr/bin/env python2
import rospy
import time
from threading import Thread
from simple_settings import settings
from random import random
from rosJason import *

my_name = settings.MY_NAME
drone_number = 2
status = "busy"

rosj = RosJason(my_name)

def wait_drones():
    while True:
        rosj.broadcast('askOne', 'online(X)')
        print(rosj.messages)
        if "online" in rosj.messages and len(rosj.messages["online"])==drone_number:
            break
        else:
            rosj.message_event.clear()
            rosj.message_event.wait(2.0)


def goToPos(lat, long, alt):
    rosj.act("setpoint", [str(lat), str(long), str(alt)])
    tol = 0.00001
    while abs(float(rosj.perceptions['global_pos'][0]) - lat) > tol or abs(
            float(rosj.perceptions['global_pos'][1]) - long) > tol:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def takeOff(alt):
    rosj.act("takeoff", ["5"])
    while 'altitude' not in rosj.perceptions:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

    while abs(float(rosj.perceptions['altitude'][0]) - alt) > 0.1:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def rtl():
    rosj.act("set_mode", ["RTL"])
    tol = 0.00001
    while abs(float(rosj.perceptions['global_pos'][0]) - float(rosj.perceptions['home_pos'][0])) > tol or abs(
            float(rosj.perceptions['global_pos'][1]) - float(rosj.perceptions['home_pos'][1])) > tol or abs(float(rosj.perceptions['altitude'][0]) - 0) > 0.1:
        rosj.perception_event.clear()
        rosj.perception_event.wait()

def deliverBuoys():
    while True:
        if "victim_in_need" in rosj.messages and len(rosj.messages["victim_in_need"]) > 0:
            rosj.message_lock.acquire()
            victim = rosj.messages["victim_in_need"].pop(0)
            rosj.message_lock.release()
            victim = victim.split(',')
            rescueVictm(float(victim[0]), float(victim[1]), float(victim[2]))
        else:
            rosj.message_event.clear()
            rosj.message_event.wait(1.0)

def rescueVictm(n, lat, long):

    rosj.act("set_mode", ["GUIDED"])
    rosj.act("arm_motors", ["True"])

    takeOff(5)
    goToPos(lat, long, 25);
    print("Droping buoy to victim" + "victim("+ str(n) + "," + str(lat) + "," +str(long)+")")
    rtl()
    print("Landed! beginning charging and buoy replacement!")
    time.sleep(3)

# def negotiation():
#     while True:
#         if countBel("victim_in_need") > 0:
#         # if "victim_in_need" in messages and len(messages["victim_in_need"]) > 0:
#             victim = pop("victim_in_need", 0)
#
#             propose(victim[0])
#             time.sleep(2)
#             L = get_proposal(N)
#             Winner = choose_proposal(N, L)
#
# def propose(N):
#     if status == "ready":
#         R = random()
#         addBB("propose", [my_name, N, R])
#         broadcast("tell", parseString("propose", [my_name, N, R]))
#     else:
#         print("I am busy")
#
# def get_proposal(N):
#     proposals = findall("propose")
#     return [p for p in proposals if p[1]==N]
#
# def choose_proposal(N, L):
#     proposal = None
#     if len(L) >0:
#         def takeThird(elem):
#             return elem[2]
#         L.sort(key=takeThird)
#         proposal = L[0]
#     return proposal

# def check_winner(N, Winner):
#     if Winner == my_name:
#         print("I am responsible for rescuing victim " + str(N))


if __name__ == '__main__':
    print("Starting python Agent node.")
    rospy.init_node('Agent')

    wait_drones()
    # thread_negotiation = Thread(target = negotiation)
    # thread_negotiation.start()
    deliverBuoys()
    # thread_negotiation.join()
