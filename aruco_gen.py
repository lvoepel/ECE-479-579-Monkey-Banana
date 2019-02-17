#!/usr/bin/python2
# From http://www.philipzucker.com/aruco-in-opencv/
import numpy as np
import cv2
import cv2.aruco as aruco
 
 
'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''
 
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
print(aruco_dict)
# second parameter is id number
# last parameter is total image size
monkey = aruco.drawMarker(aruco_dict, 1, 700)
cv2.imwrite("monkey.jpg", monkey)

banana = aruco.drawMarker(aruco_dict, 2, 700)
cv2.imwrite("banana.jpg", banana)

ramp = aruco.drawMarker(aruco_dict, 3, 700)
cv2.imwrite("ramp.jpg", ramp)




cv2.imshow('frame', monkey)
cv2.waitKey(0)
cv2.destroyAllWindows()
