#!/usr/bin/env python

#listens to directions given by plan publisher and publishes twist values based on them.

import rospy
from time import time
from std_msgs.msg import Int32
from std_msgs.msg import String
import math



#if robot says its "done" then publish the next message
def directions_callback(msg):
    degrees = msg.data    
    status.publish("turning")
    
    print("You're facing: " + str(old_deg))
        print("You should be facing: " + str(new_deg))
        
        print("Turn " + str(target) + " degrees!")

        file
        direction.publish(0)

rospy.init_node('plan_publisher')

status = rospy.Publisher ('/robo_status', Int32, queue_size=1)
direction = rospy.Publisher("/direction_command", String, directions_callback))

r = rospy.Rate(10)

while not rospy.is_shutdown():
        
    direction.publish(0)

    r.sleep()
