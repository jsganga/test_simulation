'''
beginning control of flappy bird game by calling the flappy module, and initializing the robot state

Jake Sganga 11/20/16
'''
import numpy as np
import time
# import pygame
import time
from flappy_bird.flappy import flappy
from control.reinforcement_learning import RL, time_series_reward

def control_flappy(game_replay=False,
                   real_time=True):
  game = flappy(real_time=real_time)
  rl = RL(initial_state=game.get_state())
  control_loop(game, real_time, rl)
  if game_replay:
    game.graphics.game_replay()


def control_loop(game, real_time, rl):
  frame_timer = time.perf_counter()
  i_games = 0
  # clock = pygame.time.Clock()
  total_batches = 1000
  games_per_batch = 64
  discount = 0.95

  actual_real_time = real_time

  for batch in range(total_batches):
    
    batch_states = []
    batch_next_states = []
    batch_actions = []
    batch_action_seq = []
    batch_rewards = []
    batch_reward_seq = []
    batch_score = []

    for i_games in range(games_per_batch):
      # print("Game number ", i_games)
      if not i_games:
        real_time = True
        game.real_time=True
      else:
        real_time = actual_real_time
        game.real_time = actual_real_time
      game.initialize_game()
      
      states = []
      next_states = []
      actions = []  
      rewards = []
      scores = []

      while not game.game_over:
        action = 0
        state = game.get_state()
        if i_games and np.random.random() < 0.1:#np.min([.25, 0.9 - .005*batch]) and i_games:
          # explore
          if np.random.random() < 0.45:#np.min([0.8, 0.4 + .0005*batch]):
            game.flap()
            action = 1
          # if not rl.policy(state):
          #   game.flap()
          #   action = 1
        
        elif rl.policy(state):
          game.flap()
          action = 1
          # if real_time:
          #   print("FLAP!!")

        game.move_screen()
        game.check_crash()
        game.update_score()

        # reward = game.score if not game.game_over else -10
        # reward = 10 if not game.game_over else -10
        reward = 1 + 10*game.score if not game.game_over else -1000

        states.append(state)
        actions.append(action)
        rewards.append(reward)
        scores.append(game.score)

        if real_time:
          game.graphics.check_exit() # necessary or won't update screen!!!
          game.graphics.update_display()
          # clock.tick(game.fps)
          time.sleep(1. / game.fps)
          # pygame.time.delay(2000)

      next_states = states[1:].copy()
      next_states.append(states[0]*0) # all zeros=end state

      # policy grad action sequences
      len_actions = 50
      action_sequences = []
      reward_sequences = []
      for i_state in range(len(states)):
        action_seq = np.zeros(len_actions)
        reward_seq = np.zeros(len_actions)
        
        i_last = np.min(i_state + len_actions, len(states))
        len_action_seq = i_last - i_state
        if len_actions_seq:
          action_seq[:len_actions_seq] = actions[i_state:i_last]
          reward_seq[:len_actions_seq] = rewards[i_state:i_last]

        action_sequences.append(action_seq)
        reward_sequences.append(reward_seq)


      # process rewards
      rewards = time_series_reward(rewards, discount=discount)

      # fill batches
      batch_states += states
      batch_next_states += next_states
      batch_actions += actions
      batch_action_seq += action_sequences
      batch_rewards += list(rewards)
      batch_reward_seq += reward_sequences
      batch_score.append(np.max(scores))

    # batch finished, train
    print("batch number {}, avg reward {:0.3f}, max score: {}, n examples {}".format(
      batch, np.mean(batch_rewards), np.max(batch_score), len(batch_states)))
    # import pdb; pdb.set_trace()
    #rl.update_q_function(batch_states, batch_actions, batch_rewards, next_states=batch_next_states)
    # rl.update_q_function(batch_states, batch_actions, batch_rewards)
    rl.update_policy(batch_states_seq, batch_actions_seq, batch_rewards_seq)

  import pdb; pdb.set_trace()




