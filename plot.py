
import numpy as np 
import matplotlib.pyplot as plt

from agent import RandomAgent,Greedy
from arena import fight,compute_win_rate

from MCTS import MCTSAgent,epsGreedy_TreePolicy,UCT,T_Softmax 
from eval import RandomEval



# MCTS 




def MCTS_time(rules,Tmin=1e-4,Tmax=1e-1,Nvalues=10,repeat=100):

    random_agent=RandomAgent()
    random_eval=RandomEval(random_agent,1) 
    tree_policy_greedy=UCT(1)

    T=np.exp(np.linspace(np.log(Tmin),np.log(Tmax),Nvalues))

    winrates=[]
    for t in T:
        agent_MCTS=MCTSAgent(random_eval,tree_policy_greedy,compute_budget=t)
        wr=compute_win_rate(agent_MCTS,random_agent,rules,repeat=repeat)
        winrates.append(wr)
    winrates=np.array(winrates)

    plt.figure()
    plt.plot(T,winrates)
    plt.show()


def MCTS_bandit(rules,t=1e-2,repeat=100):

    random_agent=RandomAgent()
    random_eval=RandomEval(random_agent,1) 

    uct=UCT(0.1)
    MCTS_uct=MCTSAgent(random_eval,uct,compute_budget=t)

    greedy=epsGreedy_TreePolicy(0)
    MCTS_greedy=MCTSAgent(random_eval,greedy,compute_budget=t)

    random=epsGreedy_TreePolicy(1)
    MCTS_random=MCTSAgent(random_eval,random,compute_budget=t)

    eps_greedy=epsGreedy_TreePolicy(0.1)
    MCTS_eps_greedy=MCTSAgent(random_eval,eps_greedy,compute_budget=t)

    print('UCT vs greedy')
        
    wr=compute_win_rate(MCTS_uct,MCTS_greedy,rules,repeat=repeat)
    print(wr)
            
    print('UCT vs random')

    wr=compute_win_rate(MCTS_uct,MCTS_random,rules,repeat=repeat)
    print(wr)

    print('UCT vs eps_greedy')

    wr=compute_win_rate(MCTS_uct,MCTS_eps_greedy,rules,repeat=repeat)
    print(wr)



    print('Greedy vs Random')

    wr=compute_win_rate(MCTS_greedy,MCTS_random,rules,repeat=repeat)
    print(wr)

    print('Greedy vs eps_greedy')

    wr=compute_win_rate(MCTS_greedy,MCTS_eps_greedy,rules,repeat=repeat)
    print(wr)

    print('Random vs eps_greedy')

    wr=compute_win_rate(MCTS_random,MCTS_eps_greedy,rules,repeat=repeat)
    print(wr)

    

def MCTS_tree_mater(rules,Tmin=1e-4,Tmax=1e-1,Nvalues=10,repeat=100):

    random_agent=RandomAgent()
    random_eval=RandomEval(random_agent,1) 
    ennemy_agent=Greedy(random_eval)

    tree_policy_greedy=UCT(1)

    T=np.exp(np.linspace(np.log(Tmin),np.log(Tmax),Nvalues))

    winrates=[]
    for t in T:
        agent_MCTS=MCTSAgent(random_eval,tree_policy_greedy,compute_budget=t)
        wr=compute_win_rate(agent_MCTS,ennemy_agent,rules,repeat=repeat)
        winrates.append(wr)
    winrates=np.array(winrates)

    plt.figure()
    plt.plot(T,winrates)
    plt.show()