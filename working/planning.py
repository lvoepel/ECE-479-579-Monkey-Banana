import numpy as np
from pyswip import Prolog
from colorama import Fore, Back, Style
import cv2

#simulates steps taken while the monkey is pushing the box
def pushing(steps, prologg):
    prolog = prologg
    pushed = list(prolog.query("pushto(monkey, box, [Xm, Ym], [Xb, Yb], Dir)"))
    while(pushed):
        for push in pushed:
            steps.append(push)
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(push['Xm']) +"," + str(push['Ym']) + "])")
            prolog.retractall("at(box, [Xb,Yb])")
            prolog.assertz("at(box,[" + str(push['Xb']) +"," + str(push['Yb']) + "])")
            print("Push!")
            
        pushed = list(prolog.query("pushto(monkey, box, [Xm, Ym], [Xb, Yb], Dir)"))
    
    return steps

#Gerates options for monkey to move towards goal
#Goal is a space directly adjacent to box opposite of banana
#Box should be between monkey and banana
def moving(steps, prologg):
    prolog = prologg
    moves = list(prolog.query("moveto(monkey, [Xm, Ym], Dir)"))
    
    for move in moves:
        prevM = list(prolog.query("at(monkey, [Xm, Ym])"))[0]
        prevB = list(prolog.query("at(box, [Xb, Yb])"))[0]
        print("starting at:" + str(prevM['Xm']) + "," + str(prevM['Ym']))
        #if direction is 0 then we dont move. 
        #Box either needs to be pushed or 
        #Box is already under banana and monkey has to climb
        if move['Dir'] == 0:
            #attempt to push the box first, if no push occurs 
            #nothing is lost but time. 
            steps = pushing(steps, prolog)
            #attempt to move again If box wasn't pushed or is under
            #banana nothing happens
            steps = moving(steps, prolog)
            #Attempt to approach ramp on climbing side
            steps = upRamp(steps, prolog)

            #return monkey and box to states they were in during previous call
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(prevM['Xm']) +"," + str(prevM['Ym']) + "])")
            prolog.retractall("at(box, [Xb,Yb])")
            prolog.assertz("at(box,[" + str(prevB['Xb']) +"," + str(prevB['Yb']) + "])")

            return steps

        #if we are able to move
        else:
            #add move to current list of steps
            steps.append(move)

            #change monkey position to where next option is
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(move['Xm']) +"," + str(move['Ym']) + "])")

            #move again at the current position
            moving(steps, prolog)

            #Return monkey position to previous value
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(prevM['Xm']) +"," + str(prevM['Ym']) + "])")

            return steps
    return steps

#Calls move to climb which is a special version of move. 
#monkey will move to the side of the box where the ramp is located 
#in order to climb up and get the banana
def upRamp(steps, prologg):
    prolog = prologg
    moves = list(prolog.query("movetoclimb(monkey, [Xm, Ym], Dir)"))
    #i = 1
    for move in moves:
        prevM = list(prolog.query("at(monkey, [Xm, Ym])"))[0]
        prevB = list(prolog.query("at(box, [Xb, Yb])"))[0]
        #print(i)
        #i = i + 1
        print("starting at:" + str(prevM['Xm']) + "," + str(prevM['Ym']))
        if move['Dir'] == 0:
            climbUp(steps, prolog)
            print("Here!")
            print("Steps to return")
            for step in steps:
                print(step['Xm'], step['Ym'])
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(prevM['Xm']) +"," + str(prevM['Ym']) + "])")
            prolog.retractall("at(box, [Xb,Yb])")
            prolog.assertz("at(box,[" + str(prevB['Xb']) +"," + str(prevB['Yb']) + "])")
            return steps
        else:
            steps.append(move)
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(move['Xm']) +"," + str(move['Ym']) + "])")
            upRamp(steps, prolog)
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(prevM['Xm']) +"," + str(prevM['Ym']) + "])")
            return steps
    #print("went up ramp!")
    return steps

def climbUp(steps, prologg):
    prolog = prologg
    climbed = list(prolog.query("climbup(monkey, [Xm, Ym], Dir)"))
    while(climbed):
        for climb in climbed:
            steps.append(climb)
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(climb['Xm']) +"," + str(climb['Ym']) + "])")
            print("climb!")
            
        climbed = list(prolog.query("climbup(monkey, [Xm, Ym], Dir)"))
    
    return steps
    
def externalCall(positions):
    cap = cv2.VideoCapture(0)
    print(positions.monkey.x, positions.monkey.y)
    print(positions.banana.x, positions.banana.y)
    print(positions.ramp.x, positions.ramp.y)
    cap.release()

    #initialize prolog
    prolog = Prolog()
    prolog.consult("monkey.pl")
    
    #gX = str(raw_input("Enter X size of graph: "))
    #gY = str(raw_input("Enter Y size of graph: "))
    gX = 7
    gY = 9
    #get User input for where everything is(will be changed to opencv)
    mX = int(positions.monkey.x)
    mY = int(positions.monkey.y)
    #mX = 4
    #mY = 2

    baX = int(positions.banana.x)
    baY = int(positions.banana.y)
    #boX = 3
    #boY = 1

    boX = int(positions.ramp.x)
    boY = int(positions.ramp.y)
    
    boD = int(raw_input("Enter box direction: "))
    #baX = 2
    #baY = 2

    scale = 80
    #assert positions of everything
    prolog.assertz("at(monkey,["+str(mX) +"," + str(mY) +"])")
    prolog.assertz("at(box,["+str(boX) +"," + str(boY) +"])")
    prolog.assertz("at(banana,["+str(baX) +"," + str(baY) +"])")
    prolog.assertz("box_direction("+str(boD) +")")

    steps = []
    #call to moving which produces a list of steps based on where we can move to 
    steps = moving(steps, prolog)
    plan = open("plan.txt", "w")
    #print out list version of plan
    print("Plan:")
    if steps:
        for step in steps:
            print(step['Xm'], step['Ym'], step["Dir"])
            plan.write(str(step)+'\n')
    plan.close()
    img = np.ones((gX*scale+3,gY*scale+3,3), np.uint8)*255
    x = 0
    y = 0
    #draw grid
    while y < gY*scale:
        while x < gX*scale:
            cv2.rectangle(img,(y,x),(y+scale,x+scale),(0,0,0),3)
            #cv2.rectangle(img,(y+10,x+10),(y+40,x+40),(0,255,0),3)
            print("currently at " + str(x) +','+ str(y))
            print("monkey at " + str(mX) +','+ str(mY))
            print("result " + str(x/scale) +','+ str(y/scale))
            if(mX == x/scale and mY == y/scale):
                print("monkey here " + str(x) +','+ str(y))
                cv2.rectangle(img,(x+10,y+10),(x+scale-10,y+scale-10),(19,69,139),3)
            elif(boX == x/scale and boY == y/scale):
                cv2.rectangle(img,(x+10,y+10),(x+scale-10,y+scale-10),(0,0,255),3)
            elif(baX == x/scale and baY == y/scale):
                cv2.rectangle(img,(x+10,y+10),(x+scale-10,y+scale-10),(0,255,255),3)
            x = x + scale
        x = 0
        y = y + scale
    i = 0
    for step in steps:
        i = i + 1
        x = step['Xm']*scale+(scale/2)
        y = step['Ym']*scale+(scale/2)
        if step["Dir"] == 1:
            cv2.line(img,(x,y),(x,y-scale),(255-i*15,0,0),5)
        elif step["Dir"] == 2:
            cv2.line(img,(x,y),(x-scale,y),(255-i*15,0,0),5)
        elif step["Dir"] == 3:
            cv2.line(img,(x,y),(x,y+scale),(255-i*15,0,0),5)
        elif step["Dir"] == 4:
            cv2.line(img,(x,y),(x+scale,y),(255-i*15,0,0),5)
    '''
    cv2.line(img,(5*50+25,5*50+25),(5*50+25,5*50+75),(255,0,0),5)
    cv2.line(img,(5*50+25,5*50+25),(5*50+75,5*50+75),(255,0,255),5)
    cv2.line(img,(5*50+25,5*50+25),(5*50+75,5*50+25),(0,0,255),5) 
    '''
    while True:
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__' :
    #initialize prolog
    prolog = Prolog()
    prolog.consult("monkey.pl")
    
    #gX = str(raw_input("Enter X size of graph: "))
    #gY = str(raw_input("Enter Y size of graph: "))
    gX = 7
    gY = 9
    #get User input for where everything is(will be changed to opencv)
    mX = int(raw_input("Enter Monkey X: "))
    mY = int(raw_input("Enter Monkey Y: "))
    #mX = 4
    #mY = 2

    boX = int(raw_input("Enter box X: "))
    boY = int(raw_input("Enter box Y: "))
    boD = int(raw_input("Enter box direction: "))
    #boX = 3
    #boY = 1

    baX = int(raw_input("Enter banana X: "))
    baY = int(raw_input("Enter banana Y: "))
    #baX = 2
    #baY = 2

    scale = 80
    #assert positions of everything
    prolog.assertz("at(monkey,["+str(mX) +"," + str(mY) +"])")
    prolog.assertz("at(box,["+str(boX) +"," + str(boY) +"])")
    prolog.assertz("at(banana,["+str(baX) +"," + str(baY) +"])")
    prolog.assertz("box_direction("+str(boD) +")")

    steps = []
    #call to moving which produces a list of steps based on where we can move to 
    steps = moving(steps, prolog)
    plan = open("plan.txt", "w")
    #print out list version of plan
    print("Plan:")
    if steps:
        for step in steps:
            print(step['Xm'], step['Ym'], step["Dir"])
            plan.write(str(step)+'\n')
    plan.close()
    img = np.ones((gX*scale+3,gY*scale+3,3), np.uint8)*255
    x = 0
    y = 0
    #draw grid
    while y < gY*scale:
        while x < gX*scale:
            cv2.rectangle(img,(y,x),(y+scale,x+scale),(0,0,0),3)
            #cv2.rectangle(img,(y+10,x+10),(y+40,x+40),(0,255,0),3)
            print("currently at " + str(x) +','+ str(y))
            print("monkey at " + str(mX) +','+ str(mY))
            print("result " + str(x/scale) +','+ str(y/scale))
            if(mX == x/scale and mY == y/scale):
                print("monkey here " + str(x) +','+ str(y))
                cv2.rectangle(img,(x+10,y+10),(x+scale-10,y+scale-10),(19,69,139),3)
            elif(boX == x/scale and boY == y/scale):
                cv2.rectangle(img,(x+10,y+10),(x+scale-10,y+scale-10),(0,0,255),3)
            elif(baX == x/scale and baY == y/scale):
                cv2.rectangle(img,(x+10,y+10),(x+scale-10,y+scale-10),(0,255,255),3)
            x = x + scale
        x = 0
        y = y + scale
    i = 0
    for step in steps:
        i = i + 1
        x = step['Xm']*scale+(scale/2)
        y = step['Ym']*scale+(scale/2)
        if step["Dir"] == 1:
            cv2.line(img,(x,y),(x,y-scale),(255-i*15,0,0),5)
        elif step["Dir"] == 2:
            cv2.line(img,(x,y),(x-scale,y-scale),(255-i*15,0,0),5)
        elif step["Dir"] == 3:
            cv2.line(img,(x,y),(x-scale,y),(255-i*15,0,0),5)
        elif step["Dir"] == 4:
            cv2.line(img,(x,y),(x-scale,y+scale),(255-i*15,0,0),5)
        elif step["Dir"] == 5:
            cv2.line(img,(x,y),(x,y+scale),(255-i*15,0,0),5)
        elif step["Dir"] == 6:
            cv2.line(img,(x,y),(x+scale,y+scale),(255-i*15,0,0),5)
        elif step["Dir"] == 7:
            cv2.line(img,(x,y),(x+scale,y),(255-i*15,0,0),5)
        elif step["Dir"] == 8:
            cv2.line(img,(x,y),(x+scale,y-scale),(255-i*15,0,0),5)
    '''
    cv2.line(img,(5*50+25,5*50+25),(5*50+25,5*50+75),(255,0,0),5)
    cv2.line(img,(5*50+25,5*50+25),(5*50+75,5*50+75),(255,0,255),5)
    cv2.line(img,(5*50+25,5*50+25),(5*50+75,5*50+25),(0,0,255),5) 
    '''
    while True:
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

    
