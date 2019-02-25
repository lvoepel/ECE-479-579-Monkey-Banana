# File: ServoMoment.py
#
# Date: 2/23/2019
# Portland State University
#############################################################
from global_File import *


class ServoMovement:
    def __init__(self, input_servo_connection):
        self.input_object = input_servo_connection

    """
    def pick_up(self):
        # time.sleep(1.5)
        self.input_object.goto(5, 85, speed=120, degrees=True)
        time.sleep(1)

    def place(self):
        # time.sleep(1.5)
        self.input_object.goto(5, 20, speed=120, degrees=True)
        time.sleep(1)
    """
    def reset(self):
        print("Reset Positions")
        self.input_object.goto(6, 0, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(7, 0, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(8, 0, speed=SERVO_SPEED, degrees=True)
        time.sleep(0.5)
        self.input_object.goto(9, -90, speed=SERVO_SPEED, degrees=True)
        time.sleep(4)
        self.input_object.goto(10, 0, speed=SERVO_SPEED, degrees=True)
        time.sleep(4)

    def open_hand(self):
        print("Claw Opened")
        serial_connection.goto(10, 30, speed=SERVO_SPEED, degrees=True)
        time.sleep(4)

    """
def pick_and_place(initial_location, destination):
    #servo_class.move_to(initial_location)
    #servo_class.pick_up()
    #servo_class.reset()
    #servo_class.move_to(destination)
    #servo_class.place()
    #servo_class.reset()
    """


if __name__ == "__main__":

    # open camera
    serial_connection: Connection = Connection(port="COM14", baudrate=1000000)

    # initalize objects
    servo_class = ServoMovement(serial_connection)
    # reset the hand before
    servo_class.reset()
    servo_class.open_hand()


