''' qlearning agent '''
import random
import pickle

from boardAI import AbstractPlayer
from connect4 import OptimalBoard

from .qlearning import QLearning

class QLearningPlayer(AbstractPlayer):
    ''' qlearning agent '''
    def __init__(self, learning_rate=0.1, discount_rate=0.9, exploit_rate=0.2, *args, **kwargs):
        self.exploit_rate = exploit_rate
        self.q = QLearning(value=0, n_actions=9, learning_rate=learning_rate, discount=discount_rate)

        super().__init__(*args, **kwargs)

    def serialize(self):
        return pickle.dumps((self.exploit_rate, self.q.serialize()))

    def deserialize(self, obj):
        if obj != None:
            self.exploit_rate, obj2 = pickle.loads(obj)
            self.q.deserialize(obj2)

    def _choose(self, state, available_actions):
        if self.is_train_mode and random.random() < self.exploit_rate:
            return random.choice(available_actions)

        ob = OptimalBoard(state)
        converted_actions = ob.convert_action_to_optimal(available_actions)
        action = self.q.rargmax(ob.board_id, converted_actions)
        return ob.convert_action_to_original(action)

    def _feedback(self, state, action, next_state, reward, done):
        ob1 = OptimalBoard(state)
        ob2 = OptimalBoard(next_state)
        self.q.learn(ob1.board_id,
                     ob1.convert_action_to_optimal(action),
                     reward,
                     ob2.board_id)
