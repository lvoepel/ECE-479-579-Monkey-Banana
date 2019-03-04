#!/usr/bin/python2
# From http://www.philipzucker.com/aruco-in-opencv/
import numpy as np
import cv2
import cv2.aruco as aruco

# Defines
gridDimensions = 5

class Object_Telemetry:
    """Position data for an individual game piece
    """
    x = -1
    y = -1
    rotation = -1
class All_Objects:
    """Position data for all the game pieces
    """
    monkey = Object_Telemetry()
    banana = Object_Telemetry()
    ramp = Object_Telemetry()

def frame_loop(cap, display=False):
    """capture aruco
    
    Arguments:
        cap {open cv capture object} -- the opencv device to view
    
    Keyword Arguments:
        display {bool} -- Print debug to stdout and display the OpenCV frame (default: {False})
    
    Returns:
        All_Objects -- An All_Objects object containing the detected positions of each object
    """
    positions = All_Objects()

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
            positions.monkey.x=x
            positions.monkey.y=y
        elif ids[count] == 2:
            print("banana")
            positions.banana.x=x
            positions.banana.y=y
        elif ids[count] == 3:
            print("ramp")
            positions.ramp.x=x
            positions.ramp.y=y
        print(x, y)

    if display is True:
        gray = aruco.drawDetectedMarkers(gray, corners)

        #print(rejectedImgPoints)
        # Add indicatiors and grid
        for i in range(1, gridDimensions):
            cv2.line(gray, ((width/gridDimensions)*i, 0), ((width/gridDimensions)*i, height), (255, 255, 0), 1, 1)
        for i in range(1, gridDimensions):
            cv2.line(gray, (0, (height/gridDimensions)*i), (width, (height/gridDimensions)*i), (255, 255, 0), 1, 1)
        # Display the resulting frame
        cv2.imshow('frame',gray)

    return positions


def main():
# Setup webcam
    cap = cv2.VideoCapture(0)
    while(True):
        positions = frame_loop(cap, True)
        print(positions.monkey.x, positions.monkey.y)
        print(positions.banana.x, positions.banana.y)
        print(positions.ramp.x, positions.ramp.y)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
