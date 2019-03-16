#!/usr/bin/env python

#Reads in a text file produced by planning.py
#interprets data on which steps robot should take and publishes
#a 32  bit int on how much robot should rotate. Subscribes to the
#robot_status topic to know whether robot has done previous action

import rospy
from time import time
import ast
from std_msgs.msg import Int32
from std_msgs.msg import String
import math

step_num = 0
steps = []
directions = {3:"North", 2:"East", 1:"South", 4:"West"}

#if robot says its "done" then publish the next message
def status_callback(msg):
    global step_num, steps
    if(step_num >= len(steps)):
        goal.publish("GOAL!")
        return
    new_dir = (steps[step_num])['Dir']
    if msg.data == "done":
        #start facing west by default
        old_dir = 2
        if step_num > 0:
            old_dir = (steps[step_num - 1])['Dir']
            print("You're currently facing: " + directions[old_dir])
        print("You should be facing: " + directions[new_dir])
        if((new_dir == old_dir + 1) or (new_dir == 4 and old_dir == 1)):
            degrees = 90
        elif((new_dir == old_dir - 1)or (new_dir == 1 and old_dir == 4)):
            degrees = -90  
        elif(old_dir == new_dir):
            degrees = 0
        else:
            degrees = 180
        print(old_dir)
        print(new_dir)
        step_num = step_num + 1
        direction.publish(degrees)

rospy.init_node('plan_publisher')

odom_msg = rospy.Subscriber ('/robo_status', String, status_callback)
direction = rospy.Publisher("/direction_command",Int32, queue_size=1)
goal = rospy.Publisher("/goal_reached",String, queue_size=1)

r = rospy.Rate(10)

plan = open("plan.txt", "r")
#steps = []
for line in plan:
    print(line)
    step = ast.literal_eval(line)
    steps.append(step)
plan.close()

if steps:
    for step in steps:
        print(step)
while not rospy.is_shutdown():
    r.sleep()
