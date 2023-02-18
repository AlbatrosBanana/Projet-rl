
### ---------------------------- Format To Define Moves ---------------------------- ###

class Position():
    def __init__(self,player):
        self.player=player

class Move():
    def __init__(self):
        pass


class Rules():
    
    def new_game(self):
        return Position()

    def valid_moves(self,position:Position):
        return [Move(),Move()]

    def next_position(self,position:Position,move:Move):
        return Position()

    def winner(self,position:Position):
        # 1 or -1 or 0 or None
        return None

    def display(self,position:Position):
        pass 

### ---------------------------- Rules for the 'Token' game ---------------------------- ###

class MoveToken(Move):
    def __init__(self,n_token_removed):
        self.n_token_removed=n_token_removed


class PositionToken(Position):
    def __init__(self,player,n_token_remaining):
        self.player=player
        self.n_token_remaining=n_token_remaining


class RulesToken(Rules):
    def __init__(self,n_start=10,n_remove_max=2,first_player=1):
        self.n_start=n_start
        self.n_remove_max=n_remove_max
        self.first_player=first_player

    def new_game(self):
        return PositionToken(self.first_player,self.n_start)

    def valid_moves(self,position:PositionToken):
        valid_moves=[]
        for k in range(1,self.n_remove_max+1):
            if position.n_token_remaining>k:
                valid_moves.append(MoveToken(k))
        return valid_moves

    def next_position(self,position:PositionToken,move:MoveToken):
        return PositionToken(-position.player,position.n_token_remaining-move.n_token_removed)

    def winner(self,position:PositionToken):

        if position.n_token_remaining>1:
            return None
        else:
            return -position.player

    def display(self, position: PositionToken):

        if position.player==1:
            print(f'player:+{position.player}  board:{  ["x" for _ in range(position.n_token_remaining)] }  '  )
        elif position.player==-1:
            print(f'player:{position.player}  board:{  ["x" for _ in range(position.n_token_remaining)] }  '  )


### ---------------------------- Rules for tic-tac-toe ---------------------------- ###

import numpy as np

class MoveTTT(Move):
    def __init__(self,i,j):
        self.i=i
        self.j=j

class PositionTTT(Position):
    def __init__(self,player,mat):
        self.player=player
        self.mat=mat

class RulesTTT(Rules):

    def new_game(self):
        return PositionTTT(1,np.zeros((3,3)))

    def valid_moves(self,position:PositionTTT):
        empty=np.argwhere(position.mat == 0)
        return [MoveTTT(index[0],index[1]) for index in empty]

    def next_position(self,position:PositionTTT,move:MoveTTT):
        new_mat=position.mat.copy()
        new_mat[move.i,move.j]=position.player
        return PositionTTT(-position.player,new_mat)

    def winner(self,position:PositionTTT):

        mat=position.mat

        # check rows
        for row in mat:
            if sum(row) == 3:
                return 1
            elif sum(row) == -3:
                return -1
        
        # check columns
        for col in mat.T:
            if sum(col) == 3:
                return 1
            elif sum(col) == -3:
                return -1
                
        # check diagonals
        diag1=mat[0][0] + mat[1][1] + mat[2][2]
        diag2=mat[0][2] + mat[1][1] + mat[2][0]

        if diag1==3 or diag2==3:
            return 1
        if diag1==-3 or diag2==-3:
            return -1

        if len(self.valid_moves(position))==0:
            return 0

        return None


    def display(self, position: PositionTTT):
        print('')
        print(position.mat)

     
### ---------------------------- Rules for checkers ---------------------------- ###


import numpy as np

class MoveCheckers(Move):
    def __init__(self,i,j,v,h):
        self.i=i
        self.j=j
        self.v=v
        self.h=h

class PositionCheckers(Position):
    def __init__(self,player,mat):
        self.player=player
        self.mat=mat

class RulesCheckers(Rules):

    def new_game(self):
        # Initialize an empty 10x10 checkerboard with all zeros
        checkerboard = np.zeros((10, 10), dtype=int)

        # Set the black pieces in the first three rows
        checkerboard[1,:-1][1::2] = 1
        checkerboard[2, 1:-1][1::2] = 1
        checkerboard[3,:-1][1::2] = 1

        checkerboard[-2, 1:-1][1::2] = -1
        checkerboard[-3,:-1][1::2] = -1
        checkerboard[-4, 1:-1][1::2] = -1

        checkerboard[:,0]+=3
        checkerboard[:,-1]+=3

        return PositionCheckers(1,checkerboard)

    def valid_moves(self,position:PositionCheckers):

        player=position.player
        board=position.mat
        valid_moves = []

        v=player

        for i in range(1,9):
            for j in range(1,9):

                if board[i][j] == player:
                    
                    # check for valid diagonal moves
                    if board[i+v][j-1] == 0:
                        move=MoveCheckers(i,j,v,-1)
                        valid_moves.append(move)
                    if board[i+v][j+1] == 0:
                        move=MoveCheckers(i,j,v,+1)
                        valid_moves.append(move)

                    # check for valid jump moves
                    if board[i+v][j-1] == -player or board[i+v][j-1] == -2*player :
                        if board[i+2*v][j-2]==0:
                            move=MoveCheckers(i,j,v,-1)
                            valid_moves.append(move)

                    if board[i+v][j+1] == -player or board[i+v][j+1] == -2*player :
                        if board[i+2*v][j+2]==0:
                            move=MoveCheckers(i,j,v,+1)
                            valid_moves.append(move)

        return valid_moves


    def next_position(self,position:PositionCheckers,move:MoveCheckers):

        player=position.player
        mat=position.mat

        new_mat=mat.copy()
        new_mat[move.i,move.j]=0

        if mat[move.i+move.v,move.j+move.h]==-player:
            new_mat[move.i+move.v,move.j+move.h]=0
            new_mat[move.i+2*move.v,move.j+2*move.h]=player
        else:
            new_mat[move.i+move.v,move.j+move.h]=player

        next_position=PositionCheckers(-player,new_mat)
        if len(self.valid_moves(next_position))==0:
            #print('Saute tour')
            #print(self.display(next_position))
            next_position=PositionCheckers(player,new_mat)
            #print(len(self.valid_moves(next_position)))

        return next_position

    def winner(self,position:PositionCheckers):
        mat=position.mat
        if np.sum(mat[0,1:-1])<0:
            return -1
        if np.sum(mat[-1,1:-1])>0:
            return 1

        if len(self.valid_moves(position))==0:
            return 0
        
        return None


    def display(self, position: PositionTTT):
        print('')
        print(position.mat[:,1:-1])
