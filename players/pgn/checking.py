''' Deep Q-Learning checking '''

# import tensorflow as tf
import tensorflow.compat.v1 as tf

import tictactoe.agent as agent
import tictactoe.utils as utils

from .agent import MyAgent

tf.disable_v2_behavior()

AGENT1_DATA_PATH = "./models/pgn1.ckpt"
AGENT2_DATA_PATH = "./models/pgn2.ckpt"


def build_agent():
    ''' build agent for learning '''
    # create pgn agent1 & agent2
    agent1 = MyAgent()
    agent2 = MyAgent()

    sess = tf.Session()
    agent1.set_session(sess)
    agent2.set_session(sess)
    sess.run(tf.global_variables_initializer())

    agent1.load(AGENT1_DATA_PATH)
    agent2.load(AGENT2_DATA_PATH)

    return agent1, agent2


def checking(env, best_player):
    ''' Policy Gradient checking '''

    agent1, agent2 = build_agent()

    dual_x = agent.DualAgent(agent1, best_player)
    dual_o = agent.DualAgent(best_player, agent2)
    dual = agent.DualAgent(agent1, agent2)
    dual.set_train_mode(False)

    for _ in range(10000):
        winner, history = utils.play(env, dual_x, recorded=True)
        if winner != 0:
            print("DUAL_X", winner, "".join([str(h) for h in history]))
            break

    for _ in range(10000):
        winner, history = utils.play(env, dual_o, recorded=True)
        if winner != 0:
            print("DUAL_O", winner, "".join([str(h) for h in history]))
            break

    for _ in range(10000):
        winner, history = utils.play(env, dual, recorded=True)
        if winner != 0:
            print("DUAL", winner, "".join([str(h) for h in history]))
            break
