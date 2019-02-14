grid([[0,4],[1,4],[2,4],[3,4],[4,4],
        [0,3],[1,3],[2,3],[3,3],[4,3],
        [0,2],[1,2],[2,2],[3,2],[4,2],
        [0,1],[1,1],[2,1],[3,1],[4,1],
        [0,0],[1,0],[2,0],[3,0],[4,0]]).

connected([X1,X1], [X2,X2]) :- (X1 is X2 - 1);
                               (Y1 is Y2 - 1).

%Program for monkey to use box to grab banana
%Assumes banana is hanging and that box is at least 1 square from edges 
%to allow for monkey to manuver and push the box

:- dynamic (
	     at/2,
	     box_loc/1,
	     banana_loc/1,
	     path/1,
         goal1/2,
         goal2/2
	    ).

start :-      retractall(at(Agent,[X,Y])),
              assert(at(box,[1,2])),
              assert(at(monkey,[0,2])),
              assert(at(banana,[3,2])),
              assert(box_direction(3)). %1,3,5,7 corresponding to N, E, S, W

%monkey should climb box if box is under banana
climbup(Dir) :- (at(box,[Xbo,Ybo]), at(monkey,[Xmo,Ymo]), at(banana,[Xba,Yba]), 
             Xbo is Xba, Ybo is Yba, box_direction(DirB)),
             ((DirB is 1, Xmo is Xbo, Ymo is Ybo + 1, Dir is 5);
              (DirB is 3, Xmo is Xbo + 1, Ymo is Ybo, Dir is 7);
              (DirB is 5, Xmo is Xbo, Ymo is Ybo - 1, Dir is 1);
              (DirB is 7, Xmo is Xbo - 1, Ymo is Ybo, Dir is 3)).

climbable :- at(box,[Xbo,Ybo]), at(banana,[Xba,Yba]), Xbo is Xba, Ybo is Yba.

climbup(Dir) :- (at(box,[Xbo,Ybo]), at(monkey,[Xmo,Ymo]), at(banana,[Xba,Yba]), 
             Xbo is Xba, Ybo is Yba, box_direction(DirB)),
             ((DirB is 1, Xmo is Xbo, Ymo is Ybo + 1, Dir is 5);
              (DirB is 3, Xmo is Xbo + 1, Ymo is Ybo, Dir is 7);
              (DirB is 5, Xmo is Xbo, Ymo is Ybo - 1, Dir is 1);
              (DirB is 7, Xmo is Xbo - 1, Ymo is Ybo, Dir is 3)).


%goal will be location which places box between monkey and banana
%this allows monkey to push towards banana
goal(X1, Y1) :- (at(box,[Xbo,Ybo]), at(banana,[Xb,Yb])), 
                 ((X1 is Xbo-1, Y1 is Ybo, Xb > Xbo);
                  (X1 is Xbo+1, Y1 is Ybo, Xb < Xbo);
                  (Y1 is Ybo-1, X1 is Xbo, Yb > Ybo);
                  (Y1 is Ybo+1, X1 is Xbo, Yb < Ybo)).

rampGoal(X1, Y1) :- (at(box,[Xbo,Ybo]), at(banana,[Xb,Yb]), 
                    Xbo is Xb, Ybo is Yb, box_direction(DirB)), 
                 ((X1 is Xbo-1, Y1 is Ybo, DirB is 7);
                  (X1 is Xbo+1, Y1 is Ybo, DirB is 3);
                  (Y1 is Ybo-1, X1 is Xbo, DirB is 5);
                  (Y1 is Ybo+1, X1 is Xbo, DirB is 1)).


pushto(monkey, box,[Xm1, Ym1],[Xbo1, Ybo1], Dir) :-
       (at(monkey,[Xm0, Ym0]),at(box,[Xbo0, Ybo0]), at(banana,[Xba, Yba])),
       ((Xm0 is Xbo0, Ym0 is Ybo0-1, Ybo0 < Yba, 
            Xbo1 is Xbo0, Ybo1 is Ybo0+1, 
            Xm1 is Xm0, Ym1 is Ym0+1, Dir is 1); %north
        (Xm0 is Xbo0, Ym0 is Ybo0+1, Ybo0 > Yba, 
            Xbo1 is Xbo0, Ybo1 is Ybo0-1, 
            Xm1 is Xm0, Ym1 is Ym0-1, Dir is 5); %south
        (Xm0 is Xbo0-1, Ym0 is Ybo0, Xbo0 < Xba, 
            Xbo1 is Xbo0+1, Ybo1 is Ybo0, 
            Xm1 is Xm0+1, Ym1 is Ym0, Dir is 3);              %east
        (Xm0 is Xbo0+1, Ym0 is Ybo0, Xbo0 > Xba, 
            Xbo1 is Xbo0-1, Ybo1 is Ybo0, 
            Xm1 is Xm0-1, Ym1 is Ym0, Dir is 7)).             %west
 

moveto(monkey,[X1, Y1], Dir) :-
        at(monkey,[X0, Y0]), at(box,[Xb, Yb]), goal(Xg, Yg),
        ((Yg is Y0, Xg is X0, X1 is Xg, Y1 is Yg, Dir is 0);

        %Moving north east
        ((Xg > X0, Yg > Y0, X1 is X0 + 1, Y1 is Y0 + 1,
            %Check that box isnt in corners to cut us off
            not((Xb is X1-1,Yb is Y1)), not((Xb is X1,Yb is Y1-1)), Dir is 2);
        %Moving South East
        (Xg > X0, Yg < Y0, X1 is X0 + 1, Y1 is Y0 - 1,
            %Check that box isnt in corners to cut us off
            not((Xb is X1,Yb is Y1+1)), not((Xb is X1-1,Yb is Y1)), Dir is 4);
        %Moving North West
        (Xg < X0, Yg > Y0, X1 is X0 - 1, Y1 is Y0 + 1,
            %Check that box isnt in corners to cut us off
            not((Xb is X1,Yb is Y1-1)), not((Xb is X1+1,Yb is Y1)), Dir is 8);
        %Moving South West
        (Xg < X0, Yg < Y0, X1 is X0 - 1, Y1 is Y0 - 1,
            %Check that box isnt in corners to cut us off
            not((Xb is X1,Yb is Y1+1)), not((Xb is X1+1,Yb is Y1)), Dir is 6);

        (Xg > X0, X1 is X0 + 1, Y1 is Y0, Dir is 3);              %east
        (Xg < X0, X1 is X0 - 1, Y1 is Y0, Dir is 7);              %west
        (Yg > Y0, X1 is X0, Y1 is Y0 + 1, Dir is 1);              %north
        (Yg < Y0, X1 is X0, Y1 is Y0 - 1, Dir is 5);             %south

        %Cases where box is directly between monkey and goal
        (Xg is X0, Yg > Yb, Y0 < Yb, X1 is X0 + 1, Y1 is Y0, Dir is 3);%east
        (Xg is X0, Yg < Yb, Y0 > Yb, X1 is X0 - 1, Y1 is Y0, Dir is 7);%west
        (Yg is Y0, Xg > Xb, X0 < Xb, Y1 is Y0 + 1, X1 is X0, Dir is 1);%north
        (Yg is Y0, Xg < Xb, X0 > Xb, Y1 is Y0 - 1, X1 is X0, Dir is 5)),%south

        %to prevent getting stuck in oposite end of box:
        not((Xg is X1, Yg > Yb, Y1 < Yb)),    %goal is right of box, avoid left
        not((Xg is X1, Yg < Yb, Y1 > Yb)),    %goal is left of box, avoid right
        not((Yg is Y1, Xg > Xb, X1 < Xb)),    %goal is above of box, avoid below
        not((Yg is Y1, Xg < Xb, X1 > Xb)),    %goal is below of box, avoid above

        not(at(box,[X1, Y1]))).

movetoclimb(monkey,[X1, Y1], Dir) :-
        at(monkey,[X0, Y0]), at(box,[Xb, Yb]), rampGoal(Xg, Yg),
        ((Yg is Y0, Xg is X0, X1 is Xg, Y1 is Yg, Dir is 0);
        %Moving north east
        ((Xg > X0, Yg > Y0, X1 is X0 + 1, Y1 is Y0 + 1,
            %Check that box isnt in corners to cut us off
            not((Xb is X1-1,Yb is Y1)), not((Xb is X1,Yb is Y1-1)), Dir is 2);
        %Moving South East
        (Xg > X0, Yg < Y0, X1 is X0 + 1, Y1 is Y0 - 1,
            %Check that box isnt in corners to cut us off
            not((Xb is X1,Yb is Y1+1)), not((Xb is X1-1,Yb is Y1)), Dir is 4);
        %Moving North West
        (Xg < X0, Yg > Y0, X1 is X0 - 1, Y1 is Y0 + 1,
            %Check that box isnt in corners to cut us off
            not((Xb is X1,Yb is Y1-1)), not((Xb is X1+1,Yb is Y1)), Dir is 8);
        %Moving South West
        (Xg < X0, Yg < Y0, X1 is X0 - 1, Y1 is Y0 - 1,
            %Check that box isnt in corners to cut us off
            not((Xb is X1,Yb is Y1+1)), not((Xb is X1+1,Yb is Y1)), Dir is 6);
        (Xg > X0, X1 is X0 + 1, Y1 is Y0, Dir is 3);              %east
        (Xg < X0, X1 is X0 - 1, Y1 is Y0, Dir is 7);              %west
        (Yg > Y0, X1 is X0, Y1 is Y0 + 1, Dir is 1);              %north
        (Yg < Y0, X1 is X0, Y1 is Y0 - 1, Dir is 5)),             %south
        not(at(box,[X1, Y1]))).




