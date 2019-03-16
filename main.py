#!/usr/bin/python2
import time
import numpy as np
import cv2
import cv2.aruco as aruco
from pyswip import Prolog
from colorama import Fore, Back, Style
# Local library import
import vision.aruco_detect as detect
import working.planning as planning

if __name__ == '__main__' :
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    for x in range(5):  # Capture multiple frames, because the first frame is always broke
        positions = detect.frame_loop(cap, False)
        print(positions.monkey.x, positions.monkey.y)
        print(positions.banana.x, positions.banana.y)
        print(positions.ramp.x, positions.ramp.y)
        time.sleep(.1)


    ret, frame = cap.read()
    #print(frame.shape) # Uncomment to determine dimensions
    width = frame.shape[1]
    height = frame.shape[0]
    gridDim = 5
    positions.monkey.x = positions.monkey.x/(width/gridDim)
    positions.banana.x = positions.banana.x/(width/gridDim)
    positions.ramp.x = positions.ramp.x/(width/gridDim)
    positions.monkey.y = positions.monkey.y/(width/gridDim)
    positions.banana.y = positions.banana.y/(width/gridDim)
    positions.ramp.y = positions.ramp.y/(width/gridDim)
    cap.release()
    planning.externalCall(positions)

    