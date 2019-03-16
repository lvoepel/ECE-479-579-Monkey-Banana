#!/usr/bin/env python

#Code modified from code found at http://www.theconstructsim.com/ros-qa-135-how-to-rotate-a-robot-to-a-desired-heading-using-feedback-from-odometry/

import rospy
from std_msgs.msg import Empty
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Twist
from time import time
from std_msgs.msg import Int32
import math

roll = pitch = yaw = 0.0
init_yaw = 500
target = 0
kp=.5

def get_rotation (msg):
    global roll, pitch, yaw, target, init_yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    #print yaw
    if target:
        if init_yaw == 500:
            init_yaw = yaw
            print("init yaw is " + str(init_yaw))
        target_rad = init_yaw + target*math.pi/180
        if target_rad > math.pi:
            target_rad = -(target_rad - math.pi)
        elif target_rad < -math.pi:
            target_rad = -(target_rad + math.pi)
        if target > 0:
            if(target_rad-yaw > 0.01):
                if(target_rad - yaw < 0.1):
                    command.angular.z = kp * .2
                else:
                    command.angular.z = kp 
            elif(target_rad-yaw < -0.01):
                if(target_rad - yaw > -0.1):
                    command.angular.z = kp * .2
                else:
                    command.angular.z = kp
            else:
                command.angular.z = 0
                target = 0
                init_yaw = 500
        elif target < 0:
            if(target_rad-yaw > 0.01):
                if(target_rad - yaw < 0.1):
                    command.angular.z = -kp * .2
                else:
                    command.angular.z = -kp
            elif(target_rad-yaw < -0.01):
                if(target_rad - yaw > -0.1):
                    command.angular.z = -kp * .2
                else:
                    command.angular.z = -kp
            else:
                command.angular.z = 0
                target = 0
                init_yaw = 500
                print("HERE!")
        move.publish(command)
        print("target deg: " + str(target_rad) + " current: " + str(yaw))

def direction_cb(msg):
    global target, init_yaw
    print("WE HAVE A DIRECTION: " + str(msg.data))
    #reset odometry
    #timer = time()
    #while time() - timer < 1:
    #    reset_odom.publish(Empty())
    print("CLEARED!")
    
    target = msg.data

rospy.init_node('rotate_robot')

odom_msg = rospy.Subscriber ('/odom', Odometry, get_rotation)
direction = rospy.Subscriber("/dir",Int32,direction_cb)
move = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=1)
reset_odom = rospy.Publisher('/mobile_base/commands/reset_odometry', Empty, queue_size=10)

r = rospy.Rate(10)
command =Twist()

while not rospy.is_shutdown():
    #quat = quaternion_from_euler (roll, pitch,yaw)
    #print quat
    # reset odometry (these messages take a few iterations to get through)

    r.sleep()
