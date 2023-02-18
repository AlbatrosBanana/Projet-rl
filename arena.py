from agent import Agent
from rules import Rules,Position


def fight_from_position(agent1:Agent,agent2:Agent,rules:Rules,position:Position,display=False):

    while rules.winner(position)==None:

        if display:
            rules.display(position)

        if position.player==1:
            move=agent1.choose_move(rules,position)
        elif position.player==-1:
            move=agent2.choose_move(rules,position) 

        position=rules.next_position(position,move)

    if display:
            rules.display(position)

    return rules.winner(position)


def fight(agent1:Agent,agent2:Agent,rules:Rules,display=False):

    position=rules.new_game()

    return fight_from_position(agent1,agent2,rules,position,display=display)

    
def compute_win_rate(agent1:Agent,agent2:Agent,rules:Rules,repeat:int):

    win1=0

    for _ in range(repeat//2):
        winner=fight(agent1,agent2,rules,display=False)
        win1+=(1+winner)/2
            

    for _ in range(repeat//2):
        winner=fight(agent2,agent1,rules,display=False)
        win1+=(1-winner)/2
    
    return win1/repeat


