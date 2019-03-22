%Program for monkey to use box to grab banana
%Assumes banana is hanging and that box is at least 1 square from edges 
%to allow for monkey to manuver and push the box

%Assign things which can be changes as "dynamic"
:- dynamic (
	     at/2,   	%Where each item is at can change after running
         goal/2,	%
         climb_goal/2	%
	    ).

%Written for testing within SWIPL
%retracts where everything is and then resets them at specified positions
start :-      retractall(at(Agent,[X,Y])),
              assert(at(box,[1,1])),
              assert(at(monkey,[1,2])),
              assert(at(banana,[2,1])),
              assert(box_direction(1)). %1,2,3,4 corresponding to N, E, S, W

rampGoal(Xb, Yb) :- (at(banana,[Xba,Yba]), box_direction(DirB)),
			((DirB is 1, Xb is Xba, Yb is Yba + 1);
              (DirB is 2, Xb is Xba + 1, Yb is Yba);
              (DirB is 3, Xb is Xba, Yb is Yba - 1);
              (DirB is 4, Xb is Xba - 1, Yb is Yba)).

%monkey should climb box if box is under banana
climbup(monkey,[X1, Y1], Dir) :- 
			(at(box,[Xbo,Ybo]), at(monkey,[Xmo,Ymo]), rampGoal(Xra, Yra), at(banana,[Xba,Yba]), 
             Xbo is Xra, Ybo is Yra, box_direction(DirB)),
			 %climbing ramp
             ((DirB is 1, Xmo is Xbo, Ymo is Ybo + 1, Dir is 3, X1 is Xbo, Y1 is Ybo);
              (DirB is 2, Xmo is Xbo + 1, Ymo is Ybo, Dir is 4, X1 is Xbo, Y1 is Ybo);
              (DirB is 3, Xmo is Xbo, Ymo is Ybo - 1, Dir is 1, X1 is Xbo, Y1 is Ybo);
              (DirB is 4, Xmo is Xbo - 1, Ymo is Ybo, Dir is 2, X1 is Xbo, Y1 is Ybo);
			 %climbing from ramp to box
			  (DirB is 1, Xmo is Xbo, Ymo is Ybo, Dir is 3, X1 is Xba, Y1 is Yba);
              (DirB is 2, Xmo is Xbo, Ymo is Ybo, Dir is 4, X1 is Xba, Y1 is Yba);
              (DirB is 3, Xmo is Xbo, Ymo is Ybo, Dir is 1, X1 is Xba, Y1 is Yba);
              (DirB is 4, Xmo is Xbo, Ymo is Ybo, Dir is 2, X1 is Xba, Y1 is Yba)).



%Used to determine if the box and banana are in same place
climbable :- at(box,[Xbo,Ybo]), rampGoal(Xba, Yba), Xbo is Xba, Ybo is Yba.


%goal will be location which places box between monkey and banana
%this allows monkey to push box towards banana
goal(X1, Y1) :- (at(box,[Xbo,Ybo]), rampGoal(Xb,Yb)), 
                 ((X1 is Xbo-1, Y1 is Ybo, Xb > Xbo);
                  (X1 is Xbo+1, Y1 is Ybo, Xb < Xbo);
                  (Y1 is Ybo-1, X1 is Xbo, Yb > Ybo);
                  (Y1 is Ybo+1, X1 is Xbo, Yb < Ybo)).

%Special type of goal for when box is under banana. 
%allows the robot to approach from ramp side
climb_goal(X1, Y1) :- (at(box,[Xbo,Ybo]), rampGoal(Xb,Yb), 
                    Xbo is Xb, Ybo is Yb, box_direction(DirB)), 
                 ((X1 is Xbo-1, Y1 is Ybo, DirB is 4);
                  (X1 is Xbo+1, Y1 is Ybo, DirB is 2);
                  (Y1 is Ybo-1, X1 is Xbo, DirB is 3);
                  (Y1 is Ybo+1, X1 is Xbo, DirB is 1)).

%Changes monkey and box position to simulate "pushing" until box is lined up with either rampgoal X or rampgoal Y
%pushes either north south east or west, direction corresponds to numerical value of Dir
pushto(monkey, box,[Xm1, Ym1],[Xbo1, Ybo1], Dir) :-
       (at(monkey,[Xm0, Ym0]),at(box,[Xbo0, Ybo0]), rampGoal(Xba, Yba)),
       ((Xm0 is Xbo0, Ym0 is Ybo0-1, Ybo0 < Yba, 
            Xbo1 is Xbo0, Ybo1 is Ybo0+1, 
            Xm1 is Xm0, Ym1 is Ym0+1, Dir is 1); %north
        (Xm0 is Xbo0, Ym0 is Ybo0+1, Ybo0 > Yba, 
            Xbo1 is Xbo0, Ybo1 is Ybo0-1, 
            Xm1 is Xm0, Ym1 is Ym0-1, Dir is 3); %south
        (Xm0 is Xbo0-1, Ym0 is Ybo0, Xbo0 < Xba, 
            Xbo1 is Xbo0+1, Ybo1 is Ybo0, 
            Xm1 is Xm0+1, Ym1 is Ym0, Dir is 2);              %east
        (Xm0 is Xbo0+1, Ym0 is Ybo0, Xbo0 > Xba, 
            Xbo1 is Xbo0-1, Ybo1 is Ybo0, 
            Xm1 is Xm0-1, Ym1 is Ym0, Dir is 4)).             %west
 
%Moves monkey without pushing box.
%monkey will attempt to approach the goal defined in goal(X,Y)
%Monkey can move in 8 directions N S E W and NE SE NW SW
%Diagonals will only be used if nothing is in the corners
moveto(monkey,[X1, Y1], Dir) :-
        at(monkey,[X0, Y0]), at(box,[Xb, Yb]), goal(Xg, Yg),
        ((Yg is Y0, Xg is X0, X1 is Xg, Y1 is Yg, Dir is 0);

        %Moving north east
        ((Xg > X0, X1 is X0 + 1, Y1 is Y0, Dir is 2);              %east
        (Xg < X0, X1 is X0 - 1, Y1 is Y0, Dir is 4);              %west
        (Yg > Y0, X1 is X0, Y1 is Y0 + 1, Dir is 1);              %north
        (Yg < Y0, X1 is X0, Y1 is Y0 - 1, Dir is 3);             %south

        %Cases where box is directly between monkey and goal
        (Xg is X0, Yg > Yb, Y0 < Yb, X1 is X0 + 1, Y1 is Y0, Dir is 2);%east
        (Xg is X0, Yg < Yb, Y0 > Yb, X1 is X0 - 1, Y1 is Y0, Dir is 4);%west
        (Yg is Y0, Xg > Xb, X0 < Xb, Y1 is Y0 + 1, X1 is X0, Dir is 1);%north
        (Yg is Y0, Xg < Xb, X0 > Xb, Y1 is Y0 - 1, X1 is X0, Dir is 3)),%south

        %to prevent getting stuck in oposite end of box:
        not((Xg is X1, Yg > Yb, Y1 < Yb)),    %goal is right of box, avoid left
        not((Xg is X1, Yg < Yb, Y1 > Yb)),    %goal is left of box, avoid right
        not((Yg is Y1, Xg > Xb, X1 < Xb)),    %goal is above of box, avoid below
        not((Yg is Y1, Xg < Xb, X1 > Xb)),    %goal is below of box, avoid above

        not(at(box,[X1, Y1]))).

%Special move for monkey where it approaches climb_goal instead of goal
movetoclimb(monkey,[X1, Y1], Dir) :-
        at(monkey,[X0, Y0]), at(box,[Xb, Yb]), climb_goal(Xg, Yg),
        ((Yg is Y0, Xg is X0, X1 is Xg, Y1 is Yg, Dir is 0);
        %Moving
        ((Xg > X0, X1 is X0 + 1, Y1 is Y0, Dir is 2);              %east
        (Xg < X0, X1 is X0 - 1, Y1 is Y0, Dir is 4);              %west
        (Yg > Y0, X1 is X0, Y1 is Y0 + 1, Dir is 1);              %north
        (Yg < Y0, X1 is X0, Y1 is Y0 - 1, Dir is 3)),             %south
        not(at(box,[X1, Y1]))).




