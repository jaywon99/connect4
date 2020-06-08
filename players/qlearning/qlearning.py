''' qlearning algorithm '''
import random
import pickle

# TODO: 질문1: 갈수 없는 것도 값을 넣어야 하나?
# TODO: too many lint fix
class QLearning:
    ''' qlearning class 
    '''
    def __init__(self, value, n_actions, learning_rate, discount):
        ''' initialize qlearning algorithm
        value: initial value
        n_actions: no of actions (in tic-tac-toe: 9)
        learning_rate: alpha in q-learning
        discount: gamma in q-learning
        exploit_rate value is covered by player (not in q-learing)
        '''
        self.init_value = value
        self.n_actions = n_actions
        self.learning_rate = learning_rate # alpha
        self.discount = discount # gamma
        self.q_scores = {}
        self.debug = False

    def deserialize(self, obj):
        if obj:
            (self.q_scores, self.learning_rate, self.discount) = pickle.loads(obj)

    def serialize(self):
        return pickle.dumps((self.q_scores, self.learning_rate, self.discount))

    def init_state(self, state):
        if state not in self.q_scores:
            self.q_scores[state] = [self.init_value] * self.n_actions

    def get(self, state, action):
        self.init_state(state)
        return self.q_scores[state][action]

    def get_available_scores(self, state, available_actions = None):
        self.init_state(state)
        if available_actions == None:
            available_actions = range(self.n_actions)
        scores = {i:self.q_scores[state][i] for i in available_actions}
        return scores

    def max(self, state, available_actions = None):
        scores = self.get_available_scores(state, available_actions)
        return max(scores.values())

    def argmax(self, state, available_actions = None):
        scores = self.get_available_scores(state, available_actions)
        return max(scores, key=scores.get)

    def rargmax(self, state, available_actions = None):
        if self.debug: print("STATE", state)
        scores = self.get_available_scores(state, available_actions)
        if self.debug: print("SCORES", scores)
        max_value = max(scores.values())
        if self.debug: print("MAX_VALUE", max_value)
        max_value_index = [k for k, v in scores.items() if v == max_value]
        if self.debug: print("MAX_VALUE_INDEX", max_value_index)
        if self.debug: print(scores, max_value, max_value_index, self.q_scores[state], available_actions)
        return random.choice(max_value_index)

    def set(self, state, action, value):
        self.init_state(state)
        if self.debug: print("SET", state, action, value)
        self.q_scores[state][action] = value

    def learn(self, state, action, reward, next_state):
        q = self.get(state, action)
        dq = self.learning_rate*(reward + self.discount*self.max(next_state) - q)
        # print(state, action, next_state, reward, q, dq)
        if self.debug: print("LEARN", state, action, reward, next_state)
        self.q_scores[state][action] = q + dq
