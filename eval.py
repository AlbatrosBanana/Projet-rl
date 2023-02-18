from rules import Move,Position,Rules
from agent import Agent
from arena import fight_from_position

### ---------------------------- Format To Define Eval ---------------------------- ###

class Eval():
    def __init__(self):
        pass

    def eval(self,rules:Rules,position:Position):
        return 0
    def __call__(self,rules:Rules,position:Position):
        return self.eval(rules,position)
        
### ---------------------------- Random Eval ---------------------------- ###

class RandomEval(Eval):

    def __init__(self,policy:Agent,repeat:int):
        self.policy=policy
        self.repeat=repeat
    
    def eval(self,rules:Rules,position:Position):
        winner=rules.winner(position)
        if winner is None:
            return sum([ fight_from_position(self.policy,self.policy,rules,position,display=False) for _ in range(self.repeat) ])/self.repeat
        else:
            return winner
