from rules import Move,Position,Rules
from numpy.random import random
import numpy as np
from random import choice
from time import time
from eval import Eval
from copy import copy
from math import log,sqrt
from scipy.special import softmax


### ------------------------ TREE ------------------------ ###


class Node():
    def __init__(self,score_sum=0,n_simu=0,move=None,ancestor=None):

        self.score_sum=score_sum
        self.n_simu=n_simu
        self.children=None
        self.move=move
        self.ancestor=ancestor
    
    def score(self):    
        if self.n_simu==0:
            return 0
        else:
            return self.score_sum/self.n_simu

### ------------------------ TREE POLICIES ------------------------ ###


class TreePolicy():
    def __init__(self):
        pass
    def choose_children(self,positon:Position,node:Node):
        return choice(node.children)

class T_Softmax():
    def __init__(self,mode='log'):
        self.mode=mode

    def choose_children(self,positon:Position,node:Node):
        N=node.n_simu

        #print(N)
        if self.mode=='log':
            T=1/np.log(N+1)
        elif self.mode=='sqrt':
            T=1/np.sqrt(N)

        children=node.children
        proba_children=softmax(np.array([child.score()/T for child in children]))
        P=np.random.multinomial(1,proba_children)
        i=0
        while P[i]!=1 :
            i+=1
        return children[i]

class epsGreedy_TreePolicy(TreePolicy):
    def __init__(self,epsilon):
        self.epsilon=epsilon

    def choose_children(self,positon:Position,node:Node):
        children=node.children
        if random()<self.epsilon:
            return choice(children)
        else:  
            player=positon.player
            children_values=[child.score() for child in children]
            return children[np.argmax(player*np.array(children_values))] 

class UCT(TreePolicy):
    def __init__(self,c):
        self.c=c

    def choose_children(self,positon:Position,node:Node):
        player=positon.player
        children=node.children
        N=node.n_simu
        ucb_score=[child.score()*player + self.c*sqrt(log(N)/child.n_simu) for child in children]
        return children[np.argmax(np.array(ucb_score))]


### ------------------------ MCTS ------------------------ ###


class MCTSAgent():

    def __init__(self,eval:Eval,tree_policy:TreePolicy,compute_budget:float):
        self.eval=eval
        self.tree_policy=tree_policy
        self.compute_budget=compute_budget

    
    def init_root(self,rules,root_position):
        self.root=Node()
        self.root_position=root_position

        # EXPANSION
        valid_moves=rules.valid_moves(root_position)
        self.root.children=[Node(score_sum=0,n_simu=0,move=move,ancestor=self.root) for move in valid_moves]

        # EVALUATION 
        for child in self.root.children:
            child_positon=rules.next_position(root_position,child.move)
            value=self.eval(rules,child_positon)
            child.score_sum=value
            child.n_simu=1

            self.root.score_sum+=value
            self.root.n_simu+=1

    def step(self,rules:Rules):

        node=self.root
        simulated_position=copy(self.root_position)

        while node.children!=None:
            # SIMULATION 
            node=self.tree_policy.choose_children(simulated_position,node)
            move=node.move
            simulated_position=rules.next_position(simulated_position,move)

        winner=rules.winner(simulated_position)
        if winner==None:
            # EXPANSION
            valid_moves=rules.valid_moves(simulated_position)
            node.children=[Node(score_sum=0,n_simu=0,move=move,ancestor=node) for move in valid_moves]

            # EVALUATION 
            for child in node.children:
                child_positon=rules.next_position(simulated_position,child.move)
                value=self.eval(rules,child_positon)
                child.score_sum=value
                child.n_simu=1

            # BACKPROPAGATION
            for child in node.children:
                value=child.score()
                ancestor=child.ancestor
                while not(ancestor is None):
                    ancestor.score_sum+=value
                    ancestor.n_simu+=1
                    ancestor=ancestor.ancestor
        else:
            value=winner
            ancestor=node
            while not(ancestor is None):
                ancestor.score_sum+=value
                ancestor.n_simu+=1
                ancestor=ancestor.ancestor


    def choose_move(self,rules:Rules,position:Position):
        
        t0=time()
        self.init_root(rules,position)
        while time()-t0<self.compute_budget:
            self.step(rules)

        children_values=[child.score() for child in self.root.children]
        chosen_child=self.root.children[np.argmax(position.player*np.array(children_values)) ] 

        return chosen_child.move




