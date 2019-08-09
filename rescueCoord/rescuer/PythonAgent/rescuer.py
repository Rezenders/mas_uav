#!/usr/bin/env python2
import rospy
import time
from threading import Thread
from threading import Event
from threading import RLock
from simple_settings import settings
from random import random
from rosJason import *

my_name = settings.MY_NAME
drone_number = 3
status = "busy"

rosj = RosJason(my_name)

victims_in_rescue = []
rescue_lock = RLock()
status_event = Event()
rescue_event = Event()
proposals = dict()

def wait_drones():
    while True:
        rosj.broadcast('askOne', 'online(X)')
        if "online" in rosj.messages and len(rosj.messages["online"])==drone_number:
            status = "ready"
            status_event.set()
            break
        else:
            rosj.message_event.wait(1.0)
            rosj.message_event.clear()

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
        if len(victims_in_rescue)>0:
            rescue_lock.acquire()
            victim = victims_in_rescue.pop(0)
            rescue_lock.release()
            rescueVictm(float(victim[0]), float(victim[1]), float(victim[2]))
        else:
            rescue_event.wait()
            rescue_event.clear()

def rescueVictm(n, lat, long):
    rosj.act("set_mode", ["GUIDED"])
    rosj.act("arm_motors", ["True"])

    takeOff(5)
    goToPos(lat, long, 25);
    print("Droping buoy to victim" + "victim("+ str(n) + "," + str(lat) + "," +str(long)+")")
    rtl()
    print("Landed! beginning charging and buoy replacement!")
    time.sleep(3)
    status = "ready"
    status_event.set()


def negotiation(status_event, rosj):
    while True:
        if "victim_in_need" in rosj.messages and len(rosj.messages["victim_in_need"]) > 0:
            status_event.wait()

            rosj.message_lock.acquire()
            victim = rosj.messages["victim_in_need"].pop(0)
            rosj.message_lock.release()
            N = victim[0]
            propose(N, rosj)
            time.sleep(2.0)
            L = get_proposal(N)
            Winner = choose_proposal(N, L)
            check_winner(N, Winner, victim)
        else:
            rosj.message_event.wait(1.0)
            rosj.message_event.clear()

def propose(N, rosj):
    R = random()
    if N not in proposals:
        proposals[N] = []
    proposals[N].append([my_name, N, R])
    rosj.broadcast("tell", parseString("propose", [my_name, N, R]))

def get_proposal(N):
    proposals_aux = [p for p in rosj.messages["propose"] if p[1] == N]
    for p in proposals_aux:
        proposals[N].append(p)
    print(proposals)
    return proposals[N]

def choose_proposal(N, L):
    proposal = None
    if len(L) >0:
        def takeThird(elem):
            return float(elem[2])
        L.sort(key=takeThird)
        proposal = L[0]
    return proposal

def check_winner(N, Winner, victim):
    print(Winner)
    if Winner[0] == my_name:
        status = "busy"
        status_event.clear()
        print("I am responsible for rescuing victim " + str(N))
        rescue_lock.acquire()
        victims_in_rescue.append(victim)
        rescue_lock.release()
        rescue_event.set()
    else:
        print("Not selected")

if __name__ == '__main__':
    print("Starting python Agent node.")
    rospy.init_node('Agent')

    wait_drones()
    thread_negotiation = Thread(target = negotiation, kwargs=dict(status_event=status_event, rosj=rosj))
    thread_negotiation.start()
    deliverBuoys()
    thread_negotiation.join()
