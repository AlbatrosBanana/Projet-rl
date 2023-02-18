from rules import Move,Position,Rules
import numpy as np
from random import choice

### ---------------------------- Format To Define Agents ---------------------------- ###

class Agent():
    def __init__(self):
        pass
    
    def choose_move(self,rules:Rules,position:Position):
        valide_moves=rules.valid_moves(position)
        return valide_moves[0]

### ---------------------------- Random Agent ---------------------------- ###

from random import choice

class RandomAgent(Agent):
    
    def choose_move(self,rules:Rules,position:Position):
        valide_moves=rules.valid_moves(position)
        return choice(valide_moves)

### ---------------------------- Greedy ---------------------------- ###

class Eval():
    def eval(self,rules:Rules,position:Position):
        return 0
    def __call__(self,rules:Rules,position:Position):
        return self.eval(position)


class Greedy():

    def __init__(self,eval:Eval):
        self.eval=eval

    def choose_move(self,rules:Rules,position:Position):
        valide_moves=rules.valid_moves(position)
        children=[ rules.next_position(position,move) for move in valide_moves]
        children_values=[self.eval(rules,child) for child in children]
        return valide_moves[np.argmax(position.player*np.array(children_values))] 

    



    