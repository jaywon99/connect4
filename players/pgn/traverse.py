import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

import tictactoe.gym as gym
import tictactoe.agent as agent
import tictactoe.test_utils as utils

import tensorflow as tf

from tictactoe_dqn import TicTacToeDQN
from dqnagent import DQNAgent

env = gym.getEnv()
dqn1 = TicTacToeDQN()
dqn2 = TicTacToeDQN()
agent1 = DQNAgent(1, dqn1)
agent2 = DQNAgent(-1, dqn2)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
dqn1.set_session(sess)
dqn2.set_session(sess)
dqn1.load("./models/dqn1.ckpt")
dqn2.load("./models/dqn2.ckpt")

dual = agent.DualAgent(agent1, agent2)

print(utils.play(env, dual, render = True))
print(utils.test_player1(env, agent1))
print(utils.test_player2(env, agent2))

