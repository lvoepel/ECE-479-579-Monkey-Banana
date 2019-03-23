# File: Servo Movement.py
# Date: 2/23/2019
# Portland State University
#############################################################
# import rospy
# import time
# from dynamixel_msgs.msg import JointState
# from std_msgs.msg import Float64
# from std_msgs.msg import String
import os
import time
import keyboard
import serial
from pyax12.connection import Connection


"""
pub1  = rospy.Publisher('/6/command', Float64)
pub2  = rospy.Publisher('/7/command', Float64)
pub3  = rospy.Publisher('/8/command', Float64)
pub4  = rospy.Publisher('/9/command', Float64)
pub5  = rospy.Publisher('/10/command', Float64)
"""

POSSIBLE_POSITIONS = ["Reset", "Pickup", "Collect"]
a=0
b=0
c=0
d=0
e=0
flag=0
SERVO_SPEED = 75
# use the dictionary to map the positions. 2/3 Possible combinations for the arm to move
SERVO_SETTING = {"Collect":
                       {"a": 0,
                        "b":0,
                        "c": 0,
                        "d": -90,
                        "e": 60},
                 "Pickup":
                     {"a": 150,
                      "b": 0,
                      "c": 0,
                      "d": -90,
                      "e": 60,
                      },
                 "Reset":{"a": 75,
                        "b": -50,
                        "c": -100,
                        "d": -15,
                        "e": 60
                            }

                      }
        #A: 75 B: -50 C: -100 D: -15 E: 60

class ServoMovement:
    def __init__(self, input_servo_connection):
        self.input_object = input_servo_connection

    def pick_up(self):
        # time.sleep(1.5)
        print("Pick Up")
        global a,b,c,d,e

        """
        pub1.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[1]]["a"]))
        pub2.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[1]]["b"]))
        pub3.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[1]]["c"]))
        pub4.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[1]]["d"]))
        pub5.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[1]]["e"]))
        # delay between motions
        rospy.sleep(float(delay))
        
        """
        b=-25
        e=60
        self.input_object.goto(7,b, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(10, e, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)


        self.input_object.goto(6, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["a"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(8, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["c"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(9, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["d"], speed=SERVO_SPEED, degrees=True)
        time.sleep(2.0)
        b=0
        self.input_object.goto(7, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["b"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        e = 100
        self.input_object.goto(10, e, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        b=-25
        self.input_object.goto(7, b, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        print("A: {} B: {} C: {} D: {} E: {}".format(SERVO_SETTING[POSSIBLE_POSITIONS[1]]["a"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["b"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["c"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["d"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["e"]))


        """
        self.input_object.goto(6, a, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(7, b, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(8, c, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(9, d, speed=SERVO_SPEED, degrees=True)
        time.sleep(2.0)
        #e = 100
        self.input_object.goto(10, e, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        print("A: {} B: {} C: {} D: {} E: {}".format(a,
                                                     b,
                                                     c,
                                                     d,
                                                    e))

        """

        return

    def place(self):
        print("ENtered Place")
        b = -25
        e = 100
        self.input_object.goto(7, b, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(10, e, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(6, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["a"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)

        self.input_object.goto(8, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["c"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(9, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["d"], speed=SERVO_SPEED, degrees=True)
        time.sleep(2.0)
        b = 0
        self.input_object.goto(7, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["b"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        e = 60
        self.input_object.goto(10, e, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        b = -25
        self.input_object.goto(7, b, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        print("A: {} B: {} C: {} D: {} E: {}".format(SERVO_SETTING[POSSIBLE_POSITIONS[1]]["a"],
                                                     b,
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["c"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["d"],
                                                     e))



    def collect(self):
        print("Return")
        # time.sleep(1.5)
        """
             pub1.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[2]]["a"]))
             pub2.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[2]]["b"]))
             pub3.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[2]]["c"]))
             pub4.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[2]]["d"]))
             pub5.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[2]]["e"]))
             # delay between motions
             rospy.sleep(float(delay))
        """


        self.input_object.goto(6, SERVO_SETTING[POSSIBLE_POSITIONS[2]]["a"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(7, SERVO_SETTING[POSSIBLE_POSITIONS[2]]["d"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(8, SERVO_SETTING[POSSIBLE_POSITIONS[2]]["c"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(9, SERVO_SETTING[POSSIBLE_POSITIONS[2]]["d"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        print("A: {} B: {} C: {} D: {} E: {}".format(SERVO_SETTING[POSSIBLE_POSITIONS[2]]["a"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[2]]["b"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[2]]["c"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[2]]["d"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[2]]["e"]))
        return




    def reset(self):
        print("Reset Positions")
        global a,b,c,d,e

        print("A: {} B: {} C: {} D: {} E: {}".format(SERVO_SETTING[POSSIBLE_POSITIONS[0]]["a"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[0]]["b"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[0]]["c"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[0]]["d"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[0]]["e"]))


        """
                 pub1.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[0]]["a"]))
                 pub2.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[0]]["b"]))
                 pub3.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[0]]["c"]))
                 pub4.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[0]]["d"]))
                 pub5.publish(float(SERVO_SETTING[POSSIBLE_POSITIONS[0]]["e"]))
                 # delay between motions
                 rospy.sleep(float(delay))
        """

        self.input_object.goto(6, SERVO_SETTING[POSSIBLE_POSITIONS[0]]["a"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(7, SERVO_SETTING[POSSIBLE_POSITIONS[0]]["b"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        print("C: {}".format(c))
        self.input_object.goto(8, SERVO_SETTING[POSSIBLE_POSITIONS[0]]["c"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(9, SERVO_SETTING[POSSIBLE_POSITIONS[0]]["d"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(10, SERVO_SETTING[POSSIBLE_POSITIONS[0]]["e"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        print("A: {} B: {} C: {} D: {} E: {}".format(SERVO_SETTING[POSSIBLE_POSITIONS[0]]["a"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[0]]["b"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[0]]["c"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[0]]["d"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[0]]["e"]))

        a=0
        b=0
        c=0
        d=-90
        e=60




        return


def get_values():
    #print("In get Values")
    global a,b,c,d,e,flag
    if(keyboard.is_pressed("q")):
       a=a+25
       flag = 1
    elif (keyboard.is_pressed("a")):
        a=a-25
        flag = 1
    elif (keyboard.is_pressed("w")):
        b = b + 25
        flag = 1
    elif (keyboard.is_pressed("s")):
        b = b - 25
        flag = 1
    elif (keyboard.is_pressed("e")):
        c = c + 25
        flag = 1
    elif (keyboard.is_pressed("d")):
        c = c - 25
        flag = 1

    elif (keyboard.is_pressed("r")):
        d = d + 25
        flag = 1
    elif (keyboard.is_pressed("f")):
        d = d - 25
        flag = 1

    elif (keyboard.is_pressed("t")):
        e = e + 25
        flag = 1
    elif (keyboard.is_pressed("g")):
        e = e - 25
        flag = 1

    elif(keyboard.is_pressed("m")):
        servo_class.reset()



    return


def motion_play():
    servo_class.pick_up()
    servo_class.collect()
    servo_class.place()
    return

def rospy():
    rospy.init_node('Arm_movement', anonymous=True)
    # rospy.Subscriber('/Pick_Item', String, motion_play)
    # rate = rospy.Rate(20)
    # rospy.spin()

if __name__ == "__main__":
    # open COM port
    serial_connection: Connection = Connection(port="COM14", baudrate=1000000)
    # initialize objects
    servo_class = ServoMovement(serial_connection)
    # reset the hand before1
    servo_class.reset()
    motion_play()
    servo_class.reset()

    """
    while(1):
        get_values()
        if(flag==1):
            print("FLag Set")
            flag=0
            motion_play()


    try:
        rospy()
    except rospy.ROSInterruptException:
        pass
    """


 # Reset Position claw should be closed.

