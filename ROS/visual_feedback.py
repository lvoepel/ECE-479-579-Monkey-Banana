#!/usr/bin/python2
# From http://www.philipzucker.com/aruco-in-opencv/
import numpy as np
import cv2
import cv2.aruco as aruco
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String
# Defines
gridX = 4
gridY = 3
command = ""
direction = ""
moveType = ""
facing = ""
forward_val = 0
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
    global command, facing, forward_val, direction, moveType
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
        #print(j)
        #x and Y represent centers of item. Found by averaging corners
        x = (j[0] + j[2] + j[4] + j[6])/4
        y = (j[1] + j[3] + j[5] + j[7])/4
        if ids[count] == 1:
            #print("monkey")
            positions.monkey.x=x
            positions.monkey.y=y
            #if(yDifFrontM > 15 or yDifFrontM < -15):
            #    direction.publish(90)
            if(direction == "WEST"):
                print(command)
                if((j[0] - j[6] > 5 or j[0] - j[6] < -5) or (j[0] < j[2] or j[1] < j[5])):
                    if(j[0] < j[6]):
                        turn.publish(1)
                    else:
                        turn.publish(-1)
                else:
                    turn.publish(0)
                    facing = direction
            elif(direction == "EAST"):
                print(command)
                if((j[0] - j[6] > 5 or j[0] - j[6] < -5) or (j[2] < j[0] or j[5] < j[1])):
                    if(j[0] > j[6]):
                        turn.publish(1)
                    else:
                        turn.publish(-1)
                else:
                    turn.publish(0)
                    facing = direction
            elif(direction == "NORTH"):
                print(command)
                if((j[0] - j[2] > 5 or j[0] - j[2] < -5) or (j[6] < j[0] or j[1] < j[3])):
                    print("TURN")
                    if(j[0] < j[2]):
                        turn.publish(1)
                    else:
                        turn.publish(-1)
                else:
                    turn.publish(0)
                    facing = direction
            elif(direction == "SOUTH"):
                print(command)
                print(j)
                if((j[0] - j[2] > 5 or j[0] - j[2] < -5) or (j[0] < j[6] or j[3] < j[1])):
                    print("TURN")
                    if(j[0] > j[2]):
                        turn.publish(1)
                    else:
                        turn.publish(-1)
                else:
                    turn.publish(0)
                    facing = direction
            if(facing == direction):
                print(moveType)
                if(moveType == "B"):
                    if(facing == "EAST"):
                        if(forward_val == 0):
                            forward_val = (int(x)/160)*160 - 80
                        else:
                            if x > forward_val:
                                move.publish(-1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "WEST"):
                        if(forward_val == 0):
                            forward_val = (int(x)/160)*160 + 80
                        else:
                            if x < forward_val:
                                move.publish(-1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "NORTH"):
                        if(forward_val == 0):
                            forward_val = (int(y)/160)*160 + 80
                        else:
                            if y < forward_val:
                                move.publish(-1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "SOUTH"):
                        if(forward_val == 0):
                            forward_val = (int(y)/160)*160 - 80
                        else:
                            if y > forward_val:
                                move.publish(-1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                elif(moveType == "M"):
                    if(facing == "EAST"):
                        if(forward_val == 0):
                            forward_val = (int(x)/160)*160 + 240
                        else:
                            if x < forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "WEST"):
                        if(forward_val == 0):
                            forward_val = (int(x)/160)*160 - 80
                        else:
                            if x > forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "NORTH"):
                        if(forward_val == 0):
                            forward_val = (int(y)/160)*160 - 80
                        else:
                            if y > forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "SOUTH"):
                        if(forward_val == 0):
                            forward_val = (int(y)/160)*160 + 240
                        else:
                            if y < forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                elif(moveType == "C"):
                    if(facing == "EAST"):
                        if(forward_val == 0):
                            forward_val = (int(x)/160)*160 + 400
                        else:
                            if x < forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "WEST"):
                        if(forward_val == 0):
                            forward_val = (int(x)/160)*160 - 240
                        else:
                            if x > forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "NORTH"):
                        if(forward_val == 0):
                            forward_val = (int(y)/160)*160 - 240
                        else:
                            if y > forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "SOUTH"):
                        if(forward_val == 0):
                            forward_val = (int(y)/160)*160 + 400
                        else:
                            if y < forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
            
        elif ids[count] == 2:
            #print("banana")
            positions.banana.x=x
            positions.banana.y=y
        elif ids[count] == 3:
            #print("ramp")
            positions.ramp.x=x
            positions.ramp.y=y
            if(facing == direction):
                print(moveType)
                if(moveType == "P"):
                    if(facing == "EAST"):
                        if(forward_val == 0):
                            forward_val = (int(x)/160)*160 + 160 + 80
                        else:
                            if x < forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "WEST"):
                        if(forward_val == 0):
                            forward_val = (int(x)/160)*160 - 80
                        else:
                            print("we are at: " + str(x))
                            print("goal is: " + str(forward_val))
                            if x > forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "NORTH"):
                        if(forward_val == 0):
                            forward_val = (int(y)/160)*160 - 80
                        else:
                            if y > forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
                    elif(facing == "SOUTH"):
                        if(forward_val == 0):
                            forward_val = (int(y)/160)*160 + 160 + 80
                        else:
                            if y < forward_val:
                                move.publish(1)
                            else:
                                move.publish(0) 
                                forward_val = 0
                                command = ''
                                direction = ''
                                moveType = ''
                                print("DELETED COMMAND")
        #print(x, y)
        
    if display is True:
        gray = aruco.drawDetectedMarkers(gray, corners)
        
        #print(rejectedImgPoints)
        # Add indicatiors and grid
        for i in range(1, gridX):
            cv2.line(gray, ((width/gridX)*i, 0), ((width/gridX)*i, height), (255, 255, 0), 1, 1)
        for i in range(1, gridY):
            cv2.line(gray, (0, (height/gridY)*i), (width, (height/gridY)*i), (255, 255, 0), 1, 1)
        # Display the resulting frame
        cv2.imshow('frame',gray)

    return positions

def direction_cb(msg):
    global command, direction, moveType
    command = msg.data
    direction = command[1:]
    moveType = command[0]
    print("NEW COMMAND IS: " + str(command))
    print("Direction is: " + direction)
    print("move type is: " + moveType)
    return

rospy.init_node('camera_feedback')
direction = rospy.Subscriber("/direction",String, direction_cb)
turn = rospy.Publisher("/turn",Int32)
move = rospy.Publisher("/move",Int32)
status = rospy.Publisher ('/robo_status', String, queue_size=1)
#status = rospy.Publisher ('/robo_status', String, queue_size=1)

r = rospy.Rate(10)
def main():
# Setup webcam
    cap = cv2.VideoCapture(0)
    while(True):
        positions = frame_loop(cap, True)
        #print(positions.monkey.x, positions.monkey.y)
        #print(positions.banana.x, positions.banana.y)
        #print(positions.ramp.x, positions.ramp.y)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    
