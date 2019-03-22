#!/usr/bin/python2
import time
import numpy as np
import cv2
import cv2.aruco as aruco
from pyswip import Prolog

# Local library import
import aruco_detect as detect
import planning as planning

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
    gridX = 4
    gridY = 3
    positions.monkey.x = positions.monkey.x/(width/gridX)
    positions.banana.x = positions.banana.x/(width/gridX)
    positions.ramp.x = positions.ramp.x/(width/gridX)
    positions.monkey.y = positions.monkey.y/(height/gridY)
    positions.banana.y = positions.banana.y/(height/gridY)
    positions.ramp.y = positions.ramp.y/(height/gridY)
    cap.release()
    planning.externalCall(positions)

    
