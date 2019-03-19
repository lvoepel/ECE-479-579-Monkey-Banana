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
directions = {3:"NORTH", 2:"EAST", 1:"SOUTH", 4:"WEST"}

#if robot says its "done" then publish the next message
def status_callback(msg):
    global step_num, steps
    if(step_num >= len(steps)):
        goal.publish("GOAL!")
        return
    new_dir = (steps[step_num])['Dir']
    if msg.data == "done":
        
        print("You should be facing: " + directions[new_dir])
        
        step_num = step_num + 1
        direction.publish(directions[new_dir])
        pub_status.publish("Turning")

rospy.init_node('plan_publisher')

status = rospy.Subscriber ('/robo_status', String, status_callback)
pub_status = rospy.Publisher ('/robo_status', String, queue_size=1)
direction = rospy.Publisher("/direction",String, queue_size=1)
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
