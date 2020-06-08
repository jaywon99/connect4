from collections import deque
import random
import numpy as np

from .dnn import DNN

TRAINSET_SIZE = 100000
SAMPLE_SIZE = 64
DISCOUNT_RATE = 0.999

class DQN(DNN):
    ''' Deep Q Network module '''
    def __init__(self, layers=None, name="main", lr=0.0001):
        super().__init__(layers, name, lr)
        self.train_set = deque(maxlen=TRAINSET_SIZE)
        self.loss_counter = 0

    def predict_one(self, state):
        ''' predict next action '''
        return np.argmax(self.predict(state), axis=1)[0]

    def add_train_set(self, state, action, reward, next_state, done):
        ''' add to train set '''
        self.train_set.append([state, action, reward, next_state, done])

    def study(self):
        ''' learn train_set '''
        if len(self.train_set) < SAMPLE_SIZE:
            return None
        samples = random.sample(self.train_set, SAMPLE_SIZE)

        state_array = np.vstack([x[0] for x in samples])
        action_array = np.array([x[1] for x in samples])
        reward_array = np.array([x[2] for x in samples])
        next_state_array = np.vstack([x[3] for x in samples])
        done_array = np.array([x[4] for x in samples])

        x_batch = state_array
        y_batch = self.predict(state_array)

        # Write using TeX (Basic Q-Learning)
        max_next = np.max(self.predict(next_state_array), axis=1)
        q_target = reward_array + DISCOUNT_RATE * max_next * ~done_array
        y_batch[np.arange(len(x_batch)), action_array] = q_target

        loss, _ = self.update(x_batch, y_batch)

        self.loss_counter += 1
        if self.loss_counter > 100:
            self.loss_counter = 0
            # print("LOSS", loss)

        return loss
