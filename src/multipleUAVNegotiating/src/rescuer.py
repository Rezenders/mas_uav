#!/usr/bin/env python2
import rospy
import time
from threading import Thread
from threading import Event
from threading import RLock
from simple_settings import settings
from random import random
from pythonAgArch.pythonAgArch import *
import signal
import argparse

drone_number = 3
status = "busy"

victims_in_rescue = []
rescue_lock = RLock()
status_event = Event()
rescue_event = Event()
proposals = dict()

def wait_drones(agArch):
    while True:
        agArch.broadcast('askOne', 'online(X)')
        if "online" in agArch.messages and len(agArch.messages["online"])==drone_number:
            status = "ready"
            status_event.set()
            break
        else:
            agArch.message_event.wait(1.0)
            agArch.message_event.clear()

def goToPos(agArch, lat, long, alt):
    agArch.act("setpoint", [str(lat), str(long), str(alt)])
    tol = 0.00001
    while abs(float(agArch.perceptions['global_pos'][0]) - lat) > tol or abs(
            float(agArch.perceptions['global_pos'][1]) - long) > tol:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def takeOff(agArch, alt):
    agArch.act("takeoff", ["5"])
    while 'altitude' not in agArch.perceptions:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

    while abs(float(agArch.perceptions['altitude'][0]) - alt) > 0.1:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def rtl(agArch):
    agArch.act("set_mode", ["RTL"])
    tol = 0.00001
    while abs(float(agArch.perceptions['global_pos'][0]) - float(agArch.perceptions['home_pos'][0])) > tol or abs(
            float(agArch.perceptions['global_pos'][1]) - float(agArch.perceptions['home_pos'][1])) > tol or abs(float(agArch.perceptions['altitude'][0]) - 0) > 0.1:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def waitOnline(agArch):
    while 'state' not in agArch.perceptions:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

    while agArch.perceptions['state'][1] == 'False':
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def setModeGuided(agArch):
    while 'state' not in agArch.perceptions:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

    while agArch.perceptions['state'][0] != 'GUIDED':
        agArch.act("set_mode", ["GUIDED"])
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def armMotor(agArch):
    while 'state' not in agArch.perceptions:
        agArch.perception_event.clear()
        agArch.perception_event.wait()

    while agArch.perceptions['state'][2] == 'False':
        agArch.act("arm_motors", ["True"])
        agArch.perception_event.clear()
        agArch.perception_event.wait()

def deliverBuoys(agArch):
    while True:
        if len(victims_in_rescue)>0:
            rescue_lock.acquire()
            victim = victims_in_rescue.pop(0)
            rescue_lock.release()
            rescueVictm(agArch, float(victim[0]), float(victim[1]), float(victim[2]))
        else:
            rescue_event.wait()
            rescue_event.clear()

def rescueVictm(agArch, n, lat, long):
    waitOnline(agArch)
    setModeGuided(agArch)
    armMotor(agArch)

    takeOff(agArch, 5)
    goToPos(agArch, lat, long, 25);
    print("Droping buoy to victim" + "victim("+ str(n) + "," + str(lat) + "," +str(long)+")")
    rtl(agArch)
    print("Landed! beginning charging and buoy replacement!")
    time.sleep(3)
    status = "ready"
    status_event.set()


def negotiation(status_event, agArch):
    while True:
        if "victim_in_need" in agArch.messages and len(agArch.messages["victim_in_need"]) > 0:
            status_event.wait()

            agArch.message_lock.acquire()
            victim = agArch.messages["victim_in_need"].pop(0)
            agArch.message_lock.release()
            N = victim[0]
            propose(N, agArch)
            time.sleep(2.0)
            L = get_proposal(agArch, N)
            Winner = choose_proposal(N, L)
            check_winner(agArch, N, Winner, victim)
        else:
            agArch.message_event.wait(1.0)
            agArch.message_event.clear()

def propose(N, agArch):
    R = random()
    if N not in proposals:
        proposals[N] = []
    proposals[N].append([my_name, N, R])
    agArch.broadcast("tell", parseString("propose", [my_name, N, R]))

def get_proposal(agArch,N):
    if "propose" in agArch.messages:
        proposals_aux = [p for p in agArch.messages["propose"] if p[1] == N]
        for p in proposals_aux:
            proposals[N].append(p)
        return proposals[N]

def choose_proposal(N, L):
    proposal = None
    if len(L) >0:
        def takeThird(elem):
            return float(elem[2])
        L.sort(key=takeThird)
        proposal = L[0]
    return proposal

def check_winner(agArch, N, Winner, victim):
    if Winner[0] == my_name:
        status = "busy"
        status_event.clear()
        print("I am responsible for rescuing victim " + str(N))
        rescue_lock.acquire()
        victims_in_rescue.append(victim)
        rescue_lock.release()
        rescue_event.set()
        agArch.broadcast('untell', parseString("victim_in_need", victim))
    else:
        print("Not selected")

def arg_parser():
    parser = argparse.ArgumentParser(description="Python agent node")

    parser.add_argument("-n","--name", help="Agent name", nargs=1, type=str)

    args, unknown = parser.parse_known_args()
    return vars(args)

if __name__ == '__main__':
    print("Starting python Agent node.")
    rospy.init_node('python_agent', log_level=rospy.INFO)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    args = arg_parser()
    if args["name"] != None:
        my_name = args["name"][0]
    else:
        my_name = "rescuer"

    agArch = AgArch(my_name)

    wait_drones(agArch)
    thread_negotiation = Thread(target = negotiation, kwargs=dict(status_event=status_event, agArch=agArch))
    thread_negotiation.start()
    deliverBuoys(agArch)
    thread_negotiation.join()
