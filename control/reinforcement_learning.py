"""
reinforcement leanring class -- will hold the policy that says whether or not to flap. must learn policy on data
"""
import sys, os
import numpy as np
import tensorflow as tf

class RL():
  def __init__(self, initial_state):
    self.state = initial_state
    self.action = 0
    self.reward = 0
    self.nn_q_function = NN_Q_Function(initial_state)

  
  def policy(self, state):
    # policy selects action (flap/don't) based on expected outcome of each action
    return self.q_function(state, 1) > self.q_function(state, 0)

  def q_function(self, state, action):
    # learned function of expected rewards from state, action pair
    return self.nn_q_function.predict(state, action)


  def update_q_function(self, states, actions, rewards, next_states=None, discount=0.9):
    # batch operation with set of states, actions (inputs) and rewards (outputs)
    state_action_pairs = np.array([np.hstack((state, action)) for state, action in zip(states, actions)])
    rewards = np.asarray(rewards)
    self.nn_q_function.train_on_new_data(state_action_pairs, rewards, new_next_states=next_states)  

  def update_policy(self, states, actions, rewards):
   # train policy model  


class NN_Q_Function():
  """docstring for NN_Q_Function"""
  def __init__(self, initial_state, model_dir="./test/"):
    self.model_dir = model_dir
    self.build_model(input_length=len(initial_state)+1) # for len action
    self.state_action_pairs = []
    self.rewards = []
    self.next_states = []

  def build_model(self, hidden_layer_sizes=(10,10,5), input_length=21, output_length=1):
    if os.path.exists(self.model_dir):
      self.model = tf.keras.models.load_model(
        self.model_dir,
        custom_objects=None,
        compile=True
       )

    else:
      self.model = tf.keras.Sequential()
      
      self.model.add(tf.keras.layers.Dense(hidden_layer_sizes[0],
                                            input_shape=(input_length,),
                                            activation='relu'))

      for size in hidden_layer_sizes[1:]:
        self.model.add(tf.keras.layers.Dense(size))

      self.model.add(tf.keras.layers.Dense(output_length))

      optimizer = tf.keras.optimizers.Adam(0.005,decay=0)

      self.model.compile(loss='mse', optimizer=optimizer, metrics=[])


  def train_on_new_data(self, new_state_action_pairs, new_rewards, new_next_states=None):
    self.process_new_data(new_state_action_pairs, new_rewards, new_next_states)
    
    for i in range(5):
      state_action_pairs, rewards = self.get_batch_for_training()

      self.model.fit(state_action_pairs, rewards, epochs=1, batch_size=32,
        verbose=0)

  def predict(self, state, action):
    return self.model.predict(np.array([np.hstack((state, action))]))[0]


  def process_new_data(self, new_state_action_pairs, new_rewards, new_next_states=None):
    if len(self.state_action_pairs):
      self.state_action_pairs = np.vstack((self.state_action_pairs, new_state_action_pairs))
      self.rewards = np.hstack((self.rewards, new_rewards))
      if new_next_states is not None:
        self.next_states = np.vstack((self.next_states, new_next_states))
    else:
      # should consider better selection of examples 
      # (closer to terminal states at the beginning then more random)
      self.state_action_pairs = np.asarray(new_state_action_pairs)
      self.rewards = np.asarray(new_rewards)
      if new_next_states is not None:
        self.next_states = np.asarray(new_next_states)

    # else policy gradient
    # screen = 288 pixels, pipes move at 4 px per step, so 72 across, bird at 20% screen width, 
    # so round to 50 actions from pipe entering screen and bird reaching it
    # need to set 50 actions after a state as the label (negate it if crash in those 50) 
    # and ideally weight it somehow...

  def get_batch_for_training(self):
    ids_to_keep = np.arange(len(self.state_action_pairs))
    max_len=5000
    if len(self.state_action_pairs) > max_len:
      ids_to_keep = np.random.permutation(len(self.state_action_pairs))[:max_len]
      # ids_to_keep = np.arange(len(self.state_action_pairs))[-max_len:]
      low_ids_rewards = self.rewards <= np.min(self.rewards) * .8 # min is negative
      # high_ids_rewards = self.rewards >= np.max(self.rewards) * 0.8
      n_high_low = np.min([len(low_ids_rewards), int(0.2 * max_len)])
      ids_to_keep[:n_high_low] = low_ids_rewards[np.random.permutation(n_high_low)]
      # ids_to_keep[-n_high_low:] = high_ids_rewards[np.random.permutation(n_high_low)]


    
    state_action_pairs = self.state_action_pairs[ids_to_keep]
    rewards = self.rewards[ids_to_keep].copy() # don't want to overwrite reward
    if len(self.next_states):
      next_states = self.next_states[ids_to_keep]

    if len(self.next_states): # TD learning
      discount = 0.9
      for i_reward, (state, reward) in enumerate(zip(next_states, rewards)):
        if not np.sum(state) == 0:
          rewards[i_reward] += discount * np.max([self.predict(state, action) for action in [0,1]])

    return state_action_pairs, rewards



def time_series_reward(raw_rewards, discount=0.9):
  raw_rewards = np.asarray(raw_rewards).astype(float)
  rewards = raw_rewards.copy()
  for i, reward in enumerate(raw_rewards):
    rewards[i] = np.sum([raw_rewards[k] * discount ** (k-i) for k in range(i, len(raw_rewards))])
  return rewards


    