''' Double Deep Q Learning Algorithm '''

from collections import deque
import random
import numpy as np

from .dqn import DQN

TARGET_UPDATE_FREQUENCY = 16
TRAINSET_SIZE = 100000
SAMPLE_SIZE = 64
DISCOUNT_RATE = 0.95
FREQUENT_COPY = 16


class DDQN():
    ''' Double Deep Q Learning Algorithm '''

    def __init__(self, layers=None, lr=0.001):
        # super().__init__([18, 54, 54, 9], name, lr)
        self.main = DQN(layers, "main", lr)
        self.target = self.main.clone("target")
        self.train_set = deque(maxlen=TRAINSET_SIZE)
        self.study_counter = 0

    def predict_one(self, state):
        ''' predict next action '''
        return np.argmax(self.predict(state), axis=1)[0]
        # need reshape???

    def predict(self, state):
        ''' get prediction result of state '''
        return self.main.predict(state)

    def predict_by_target(self, state, actions):
        ''' predict state with target network instead of main network '''
        predict = self.target.predict(state)
        return predict[np.arange(len(predict)), actions]

    def update(self, states, rewards):
        ''' dnn update '''
        return self.main.update(states, rewards)

    def add_train_set(self, state, action, reward, next_state, done):
        ''' add train set '''
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
        # Write using TeX
        # s_t = state_array
        # s_t1 = next_state_array
        # Q(s_t, *) = self.predict(state_array)
        # Q(s_t1, *) = self.predict(next_state_array)
        # selecting the best action a with maximum Q-value of next state.
        # argmax(Q(s_t1, *)) = np.argmax(self.predict(next_state_array))
        next_predict = self.predict(next_state_array)
        # print(next_predict)
        # 이걸 row/col을 바꿔야 할지..
        next_best_action = np.argmax(next_predict, axis=1)
        # print(next_best_action)
        # calculating expected Q-value by using the action a selected above.
        q_estimated = self.predict_by_target(
            next_state_array, next_best_action)
        q_target = reward_array + DISCOUNT_RATE * q_estimated * ~done_array
        y_batch[np.arange(len(x_batch)), action_array] = q_target

        loss, _ = self.update(x_batch, y_batch)

        self.study_counter += 1
        if self.study_counter % TARGET_UPDATE_FREQUENCY == 0:
            self.copy()
            # print("LOSS", loss)

        return loss

    def copy(self):
        ''' copy network variables '''
        self.target.set_weights(self.main.get_weights())

    def save(self, filename):
        ''' save network variables '''
        self.main.save(filename)

    def load(self, filename):
        ''' load network variables '''
        self.main.load(filename)
        self.copy()
