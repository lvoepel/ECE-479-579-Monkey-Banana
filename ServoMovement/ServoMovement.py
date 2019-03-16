# File: Servo Movement.py
# Date: 2/23/2019
# Portland State University
#############################################################
from global_File import *
import keyboard

class ServoMovement:
    def __init__(self, input_servo_connection):
        self.input_object = input_servo_connection

    def pick_up(self):
        # time.sleep(1.5)
        print("Pick Up")

        self.input_object.goto(6, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["a"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(7, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["b"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(8, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["c"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(9, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["d"], speed=SERVO_SPEED, degrees=True)
        time.sleep(2.0)
        e = 100
        self.input_object.goto(10, SERVO_SETTING[POSSIBLE_POSITIONS[1]]["e"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        print("A: {} B: {} C: {} D: {} E: {}".format(SERVO_SETTING[POSSIBLE_POSITIONS[1]]["a"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["b"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["c"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["d"],
                                                     SERVO_SETTING[POSSIBLE_POSITIONS[1]]["e"]))
        return

    def collect(self):
        print("Return")
        # time.sleep(1.5)
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
        self.input_object.goto(6, SERVO_SETTING[POSSIBLE_POSITIONS[0]]["a"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(7, SERVO_SETTING[POSSIBLE_POSITIONS[0]]["b"], speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
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

        return


if __name__ == "__main__":
    # open COM port
    serial_connection: Connection = Connection(port="COM14", baudrate=1000000)
    # initialize objects
    servo_class = ServoMovement(serial_connection)
    # reset the hand before1
    servo_class.reset()

    while(1):                # Change to accept value of reached rosnode
        servo_class.pick_up()
        servo_class.collect()
        break


 # Reset Position claw should be closed.

