import sys
import getopt
import numpy as np
'''
J.Sganga 11/20/16

Playing around with creating an optimal control loop for flappy bird
will call the high level control loop, which will initialize the game
and begin the sensing and actuation commands. For now, going to try a 
bellman type recursion (memoization is key). Future work can incorp more
data driven learning like CNN's
'''
def main():
    from control.control_loop import control_flappy
    control_flappy(game_replay = False,
                   real_time   = True)

if __name__ == '__main__':
  main()
