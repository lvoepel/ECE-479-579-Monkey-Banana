#!/usr/bin/env python

#Code modified from code found at http://www.theconstructsim.com/ros-qa-135-how-to-rotate-a-robot-to-a-desired-heading-using-feedback-from-odometry/

import rospy
import time


from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from std_msgs.msg import String

direction = 0

def direction_cb(msg):
    global direction
    print("WE HAVE A DIRECTION: " + str(msg.data))
    #reset odometry
    #timer = time()
    #while time() - timer < 1:
    #    reset_odom.publish(Empty())
    r = rospy.Rate(10)
    if(msg.data == 0):
        move_cmd.angular.z = 0
        move_cmd.linear.x = 0
        move.publish(move_cmd)
        if(direction == -1):
            status.publish("done")
            direction = 0
        else:
            status.publish("backing up")
            command.publish("BACK")
    else:
        move_cmd.angular.z = 0
        move_cmd.linear.x = .1 * msg.data
        direction = msg.data
        move.publish(move_cmd)
        
    
    return
rospy.init_node('move_robot')

command = rospy.Publisher('/direction', String, queue_size=1)
forward = rospy.Subscriber("/move",Int32,direction_cb)
move = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=1)
status = rospy.Publisher ('/robo_status', String, queue_size=1)

r = rospy.Rate(10)
move_cmd = Twist ( )

while not rospy.is_shutdown():
    #quat = quaternion_from_euler (roll, pitch,yaw)
    #print quat
    # reset odometry (these messages take a few iterations to get through)

    r.sleep()
