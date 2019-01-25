import sys
import getopt
import numpy as np
import argparse
'''
J.Sganga 11/20/16

Playing around with creating an optimal control loop for flappy bird
will call the high level control loop, which will initialize the game
and begin the sensing and actuation commands. For now, going to try a 
bellman type recursion (memoization is key). Future work can incorp more
data driven learning like CNN's
'''
def main(real_time=False):
    from control.control_loop import control_flappy
    control_flappy(game_replay = False, # don't know what this does
                   real_time   = real_time)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--real_time", nargs='?', const='True')
  args = parser.parse_args()
  main(args.real_time)
