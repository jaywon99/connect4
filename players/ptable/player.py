''' prediction table agent '''

import random

from boardAI import AbstractPlayer
from connect4 import OptimalBoard

from .ptable import PredictionTable

class PredictionTablePlayer(AbstractPlayer):
    def __init__(self, exploit_rate=0.2, learning_rate=0.1, debug=False, *args, **kwargs):
        self.p_table = PredictionTable(learning_rate=learning_rate)
        self.exploit_rate = exploit_rate
        self.debug = debug
        super().__init__(*args, **kwargs)

    def serialize(self):
        return (self.exploit_rate, self.p_table.serialize())

    def deserialize(self, data):
        if data != None:
            self.exploit_rate, obj = data
            self.p_table.deserialize(obj)

    def _choose(self, state, actions):
        if self.is_train_mode and random.random() < self.exploit_rate:
            next_pos = random.choice(actions)
            if self.debug: print("SELECT", actions, "RANDOM", next_pos)

            return next_pos

        found_p = -1.0
        found_c = []
        
        ob = OptimalBoard(state)
        _id = ob.board_id
        if self.debug: print("FROM", _id)

        scores = self.p_table.lookup(_id)
        converted_actions = ob.convert_action_to_optimal(actions)
        for action in converted_actions:
            p = scores[action]
            if self.debug: print("ACTION", ob.convert_action_to_original(action), p)
            if p > found_p:
                found_p = p
                found_c = [ob.convert_action_to_original(action)]
            elif p == found_p:
                found_c.append(ob.convert_action_to_original(action))

        next_pos = random.choice(found_c)
        if self.debug: print("SELECT", found_c, found_p, next_pos)

        return next_pos

    def _episode_feedback(self, reward):
        # for winner
        history_left = reversed(self.all_history())
        (state, action, _, _, _) = next(history_left)   # pop last history and set it.
        ob = OptimalBoard(state)
        reward = self.p_table.set(ob.board_id, ob.convert_action_to_optimal(action), reward)

        for (state, action, _, _, _) in history_left:
            ob = OptimalBoard(state)
            reward = self.p_table.learn(ob.board_id, ob.convert_action_to_optimal(action), reward)

