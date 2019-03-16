import numpy as np
import random
import cv2
import math
import re
from pyax12.connection import Connection
import time
import pywin32_system32
import pyttsx3


POSSIBLE_POSITIONS = ["Reset", "Pickup", "Collect"]


SERVO_SPEED = 75
# use the dictionary to map the positions. 2/3 Possible combinations for the arm to move
SERVO_SETTING = {"Collect":
                       {"a": 0,
                        "b": 0,
                        "c": 0,
                        "d": -90,
                        "e": 60},
                 "Pickup":
                     {"a": 0,
                      "b": 50,
                      "c": 20,
                      "d": -50,
                      "e": 90,
                      },
                 "Reset":{"a": 0,
                        "b": 0,
                        "c": 0,
                        "d": -90,
                        "e": 60
                            }

                      }
