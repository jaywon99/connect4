from collections import deque
import random
import numpy as np

from .dnn import DNN

TRAINSET_SIZE = 100000
SAMPLE_SIZE = 20
DISCOUNT_RATE = 0.999

class PGN(DNN):
    ''' Policy Gradient Network module '''
    def __init__(self, layers=None, name="main", lr=0.0001):
        super().__init__(layers, name, lr)
        self.win_train_set = deque(maxlen=TRAINSET_SIZE)
        self.loss_train_set = deque(maxlen=TRAINSET_SIZE)
        self.tie_train_set = deque(maxlen=TRAINSET_SIZE)
        self.loss_counter = 0

    def predict_one(self, state):
        ''' predict next action '''
        return np.argmax(self.predict(state), axis=1)[0]

    def add_to_replay_buffer(self, reward, replay_buffer):
        ''' add to train set by reward '''
        if reward == 0: # tie
            self.tie_train_set.extend(replay_buffer)
        elif reward == 1: # win
            self.win_train_set.extend(replay_buffer)
        else:
            self.loss_train_set.extend(replay_buffer)

    def study(self):
        ''' learn train_set '''
        if len(self.win_train_set) < SAMPLE_SIZE:
            return None
        if len(self.loss_train_set) < SAMPLE_SIZE:
            return None
        if len(self.tie_train_set) < SAMPLE_SIZE:
            return None

        samples = random.sample(self.win_train_set, SAMPLE_SIZE)
        samples.extend(random.sample(self.loss_train_set, SAMPLE_SIZE))
        samples.extend(random.sample(self.tie_train_set, SAMPLE_SIZE))

        state_array = np.vstack([sample[0] for sample in samples])
        action_array = np.array([sample[1] for sample in samples])
        reward_array = np.array([sample[2] for sample in samples])

        loss, _ = self.update(state_array, action_array, reward_array)

        self.loss_counter += 1
        if self.loss_counter > 100:
            self.loss_counter = 0
            print("LOSS", loss)

        return loss
