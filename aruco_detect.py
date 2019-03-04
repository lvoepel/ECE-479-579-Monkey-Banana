#!/usr/bin/python2
# From http://www.philipzucker.com/aruco-in-opencv/
import numpy as np
import cv2
import cv2.aruco as aruco

# Defines
gridDimensions = 5


def frame_loop(cap):
    monkey_location = [-1,-1]
    banana_location = [-1,-1]
    ramp_location   = [-1,-1]

    # Capture frame-by-frame
    ret, frame = cap.read()
    #print(frame.shape) # Uncomment to determine dimensions
    width = frame.shape[1]
    height = frame.shape[0]
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    #print(corners)
    #print(ids)

    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs

    gray = aruco.drawDetectedMarkers(gray, corners)

    #print(rejectedImgPoints)
    # Add indicatiors and grid
    for i in range(1, gridDimensions):
        cv2.line(gray, ((width/gridDimensions)*i, 0), ((width/gridDimensions)*i, height), (255, 255, 0), 1, 1)
    for i in range(1, gridDimensions):
        cv2.line(gray, (0, (height/gridDimensions)*i), (width, (height/gridDimensions)*i), (255, 255, 0), 1, 1)

    for count, i in enumerate(corners):
        #x = (int(corners[i-1][0][0][0]) + int(corners[i-1][0][1][0]) + int(corners[i-1][0][2][0]) + int(corners[i-1][0][3][0])) / 4
        #y = (int(corners[i-1][0][0][1]) + int(corners[i-1][0][1][1]) + int(corners[i-1][0][2][1]) + int(corners[i-1][0][3][1])) / 4
        #print(x, y)
        j = i.ravel()
        print(j)
        x = (j[0] + j[2] + j[4] + j[6])/4
        y = (j[1] + j[3] + j[5] + j[7])/4
        if ids[count] == 1:
            print("monkey")
            monkey_location[0]=x
            monkey_location[1]=y
        elif ids[count] == 2:
            print("banana")
            banana_location[0]=x
            banana_location[1]=y
        elif ids[count] == 3:
            print("ramp")
            ramp_location[0]=x
            ramp_location[1]=y
        print(x, y)

    # Display the resulting frame
    cv2.imshow('frame',gray)

    return monkey_location,banana_location,ramp_location


def main():
# Setup webcam
    cap = cv2.VideoCapture(0)
    while(True):
        hel,llo,worl = frame_loop(cap)
        print(hel)
        print(llo)
        print(worl)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
