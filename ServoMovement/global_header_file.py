import numpy as np
import random
import cv2
import math
import re
from pyax12.connection import Connection
import time
import pywin32_system32
import pyttsx3




# HARD CODED POSITIONS
POSITION = {
    "L1": [85, 450],
    "L2": [97, 360],
    "L3": [130, 255],
    "L4": [210, 165],
    "L5": [360, 110],
    "L6": [515, 85],
    "R1": [930, 515],
    "R2": [950, 415],
    "R3": [926, 340],
    "R4": [900, 255],
    "R5": [840, 170],
    "R6": [720, 110],
}

SERVO_SPEED = 100

POSSIBLE_POSITIONS = ["R1", "R2"]

# use the dictionary to map the positions. 2/3 Possible combinations for the arm to move
SERVO_SETTING = {"R1": {1: -95.7,
                        2: 48.5,
                        3: 57.6,
                        4: 67.3},
                 "R2": {1: 91.9,
                        2: 50.6,
                        3: 51.2,
                        4: 73.2}}
