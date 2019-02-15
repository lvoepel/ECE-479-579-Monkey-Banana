import numpy as np
from pyswip import Prolog

#simulates steps taken while the monkey is pushing the box
def pushing(steps):
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
def moving(steps):
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
            steps = pushing(steps)
            #attempt to move again If box wasn't pushed or is under
            #banana nothing happens
            steps = moving(steps)
            #Attempt to approach ramp on climbing side
            steps = upRamp(steps)

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
            moving(steps)

            #Return monkey position to previous value
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(prevM['Xm']) +"," + str(prevM['Ym']) + "])")

            return steps
    return steps

#Calls move to climb which is a special version of move. 
#monkey will move to the side of the box where the ramp is located 
#in order to climb up and get the banana
def upRamp(steps):
    moves = list(prolog.query("movetoclimb(monkey, [Xm, Ym], Dir)"))
    #i = 1
    for move in moves:
        prevM = list(prolog.query("at(monkey, [Xm, Ym])"))[0]
        prevB = list(prolog.query("at(box, [Xb, Yb])"))[0]
        #print(i)
        #i = i + 1
        print("starting at:" + str(prevM['Xm']) + "," + str(prevM['Ym']))
        if move['Dir'] == 0:
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
            upRamp(steps)
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(prevM['Xm']) +"," + str(prevM['Ym']) + "])")
            return steps
    #print("went up ramp!")
    return steps

def drawGrid():
    print("Setting the Scene!")

if __name__ == '__main__' :
    #initialize prolog
    prolog = Prolog()
    prolog.consult("monkey.pl")

    #get User input for where everything is(will be changed to opencv)
    mX = str(raw_input("Enter Monkey X: "))
    mY = str(raw_input("Enter Monkey Y: "))

    boX = str(raw_input("Enter box X: "))
    boY = str(raw_input("Enter box Y: "))

    baX = str(raw_input("Enter banana X: "))
    baY = str(raw_input("Enter banana Y: "))

    #assert positions of everything
    prolog.assertz("at(monkey,["+str(mX) +"," + str(mY) +"])")
    prolog.assertz("at(box,["+str(boX) +"," + str(boY) +"])")
    prolog.assertz("at(banana,["+str(baX) +"," + str(baY) +"])")
    prolog.assertz("box_direction(3)")

    steps = []
    #call to moving which produces a list of steps based on where we can move to 
    steps = moving(steps)
    
    #print out list version of plan
    print("Plan:")
    if steps:
        for step in steps:
            print(step['Xm'], step['Ym'], step["Dir"])
    #drawGrid()
    #drawPlan()

    
