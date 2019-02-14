import numpy as np
from pyswip import Prolog

#simulates steps taken while the monkey is pushing the box
def pushing(steps):
    pushed = list(prolog.query("pushto(monkey, box, [Xm, Ym], [Xb, Yb], Dir)"))
    #print("push starts at: " + str(list(prolog.query("at(monkey, [Xm, Ym])"))))
    while(pushed):
        for push in pushed:
            steps.append(push)
            #for step in steps:
            #    print(step['Xm'], step['Ym'])
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(push['Xm']) +"," + str(push['Ym']) + "])")
            prolog.retractall("at(box, [Xb,Yb])")
            prolog.assertz("at(box,[" + str(push['Xb']) +"," + str(push['Yb']) + "])")
            print("Push!")
            
        pushed = list(prolog.query("pushto(monkey, box, [Xm, Ym], [Xb, Yb], Dir)"))
    #print("push stops at: " + str(list(prolog.query("at(monkey, [Xm, Ym])"))))
    
    return steps

def moving(steps):
    moves = list(prolog.query("moveto(monkey, [Xm, Ym], Dir)"))
    
    i = 1
    for move in moves:
        prevM = list(prolog.query("at(monkey, [Xm, Ym])"))[0]
        prevB = list(prolog.query("at(box, [Xb, Yb])"))[0]
        print(i)
        i = i + 1
        print("starting at:" + str(prevM['Xm']) + "," + str(prevM['Ym']))
        if move['Dir'] == 0:
            print("gotta push!")
            steps = pushing(steps)
            steps = moving(steps)
            steps = upRamp(steps)
            print("Steps to return")
            #for step in steps:
            #    print(step['Xm'], step['Ym'])
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(prevM['Xm']) +"," + str(prevM['Ym']) + "])")
            prolog.retractall("at(box, [Xb,Yb])")
            prolog.assertz("at(box,[" + str(prevB['Xb']) +"," + str(prevB['Yb']) + "])")
            return steps
        else:
            steps.append(move)
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(move['Xm']) +"," + str(move['Ym']) + "])")
            moving(steps)
            prolog.retractall("at(monkey, [Xm,Ym])")
            prolog.assertz("at(monkey,[" + str(prevM['Xm']) +"," + str(prevM['Ym']) + "])")
            return steps
    return steps

def upRamp(steps):
    moves = list(prolog.query("movetoclimb(monkey, [Xm, Ym], Dir)"))
    #print("getting up ramp!")
    #print("goal:" + str(list(prolog.query("rampGoal(X1, Y1)"))))
    i = 1
    for move in moves:
        prevM = list(prolog.query("at(monkey, [Xm, Ym])"))[0]
        prevB = list(prolog.query("at(box, [Xb, Yb])"))[0]
        print(i)
        i = i + 1
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
#looks at options for current monkey position

if __name__ == '__main__' :
    prolog = Prolog()
    prolog.consult("monkey.pl")
    prolog.assertz("at(monkey,[3,0])")
    prolog.assertz("at(banana,[3,2])")
    prolog.assertz("at(box,[1,1])")
    prolog.assertz("box_direction(3)")

        #print("options:")
        #options = list(prolog.query("moveto(monkey, [X, Y], Dir)"))
        #print(options)
    steps = []
    #shortest = consultOptions(steps,shortest)
    steps = moving(steps)
    print("Plan!")
    if steps:
        for step in steps:
            print(step['Xm'], step['Ym'], step["Dir"])

    
