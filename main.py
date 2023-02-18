from rules import RulesToken,RulesTTT,RulesCheckers

from plot import MCTS_time,MCTS_bandit,MCTS_tree_mater

''' # RUN TO DISPLAY A GAME OF MCTS AGAINST RANDOM AGENT
from agent import RandomAgent,Greedy
from arena import fight,compute_win_rate

from MCTS import MCTSAgent,epsGreedy_TreePolicy,UCT,T_Softmax 
from eval import RandomEval

# Display Game
rules=RulesCheckers()
wr=fight(random_agent,agent_MCTS,rules,display=True)
print(wr)
'''

# RUN TO GET THE FIGURES
  
rules=RulesCheckers()

MCTS_time(rules,Tmin=1e-3,Tmax=1e-1,repeat=100)

MCTS_bandit(rules,t=1e-1,repeat=20)

MCTS_tree_mater(rules,Tmin=1e-3,Tmax=1e-1,repeat=100)