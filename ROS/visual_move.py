#!/usr/bin/env python

#Code modified from code found at http://www.theconstructsim.com/ros-qa-135-how-to-rotate-a-robot-to-a-desired-heading-using-feedback-from-odometry/

import rospy
import time


from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from std_msgs.msg import String

direct = ''
moveType = ''
direction = 0
def move_cb(msg):
    global direction, direct, moveType
    print("WE HAVE A DIRECTION: " + str(msg.data))
    #reset odometry
    #timer = time()
    #while time() - timer < 1:
    #    reset_odom.publish(Empty())
    r = rospy.Rate(10)
    if(msg.data == 0):
        #move_cmd.angular.z = 0
        
        if(moveType != "P" or direction == -1):
            move_cmd.linear.x = 0
            move.publish(move_cmd)            
            status.publish("done moving")
            direction = 0
        else:
            status.publish("backing up")
            command.publish("B" + direct)
    else:
        #move_cmd.angular.z = 0
        move_cmd.linear.x = .08 * msg.data
        direction = msg.data
        move.publish(move_cmd)
    return

def direction_cb(msg):
    global direct, moveType
    direct = msg.data
    moveType = direct[0]
    direct = direct[1:]
    return

rospy.init_node('move_robot')

command = rospy.Publisher('/direction', String, queue_size=1)
direction = rospy.Subscriber("/direction",String, direction_cb)
go = rospy.Subscriber("/move",Int32,move_cb)
move = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=1)
status = rospy.Publisher ('/robo_status', String, queue_size=1)

r = rospy.Rate(10)
move_cmd = Twist ( )

while not rospy.is_shutdown():
    #quat = quaternion_from_euler (roll, pitch,yaw)
    #print quat
    # reset odometry (these messages take a few iterations to get through)

    r.sleep()
