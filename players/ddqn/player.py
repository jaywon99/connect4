''' DDQN learning '''

import random
import pickle

from boardAI import AbstractPlayer
from connect4 import OptimalBoard

from .ddqn import DDQN

INPUT_SIZE = 126  # 6 * 7 * 3
OUTPUT_SIZE = 7


class DDQNPlayer(AbstractPlayer):
    ''' DDQN Learning Agent '''

    # Conv2D의 사용 가능성을 리뷰해봅시다.
    def __init__(self, egreedy=0.2, hidden_layers=[378, 378], learing_rate=0.001, network_storage=None, *args, **kwargs):
        self.hidden_layers = hidden_layers
        self.network = DDQN(layers=[INPUT_SIZE]
                            + hidden_layers + [OUTPUT_SIZE], lr=learing_rate)
        self.egreedy = egreedy
        self.network_storage = network_storage
        super().__init__(*args, **kwargs)

    def serialize(self):
        # store network and configuration separate
        self.network.save(self.network_storage)
        return pickle.dumps((self.hidden_layers, self.egreedy, self.network_storage))

    def deserialize(self, obj):
        if obj is not None:
            self.network.load(self.network_storage)
            self.hidden_layers, self.egreedy, self.network_storage = pickle.loads(
                obj)

    @staticmethod
    def convert_state(state):
        ''' convert state from board style to NN style '''

        if INPUT_SIZE == 42:
            # MAKE 9 / (-1, 0, 1)로 되어있는 board state
            return state

        if INPUT_SIZE == 84:
            # [0:8] is my stone occupied
            # [9:17] is other stone occupied
            board = [1 if x == 1 else 0 for x in state]
            board.extend([1 if x == -1 else 0 for x in state])
            return board

        if INPUT_SIZE == 126:
            # [0:8] is no stone occupied
            # [9:17] is other stone occupied
            # [18:26] is my stone occupied
            # in some paper, they are using conv2d
            board = [1 if x == 0 else 0 for x in state]
            board.extend([1 if x == 1 else 0 for x in state])
            board.extend([1 if x == -1 else 0 for x in state])
            return board

        raise Exception

    def _choose(self, state, available_actions):
        optimal_board = OptimalBoard(state)
        converted_actions = optimal_board.convert_action_to_optimal(
            available_actions)
        converted_state = self.convert_state(optimal_board.optimal_board)
        ###
        if self.is_train_mode:
            if random.random() < self.egreedy:
                action = random.choice(converted_actions)
            else:
                action = self.network.predict_one(converted_state)
        else:
            action = self.network.predict_one(converted_state)

        if action not in converted_actions:
            # TODO(jaywon99): 여기에 뭐를 학습으로 넣을 지 고민
            # 아니면, predict_one에서 필터를 넣을 지 고민
            # TODO(jaywon99): put SOMETHING instead of 42
            self.network.add_train_set(
                converted_state, action, -1, self.convert_state([-1] * 42), True)  
            action = random.choice(converted_actions)

        original_action = optimal_board.convert_action_to_original(action)

        return original_action

    def _feedback(self, state, action, next_state, reward, done):
        state_ob = OptimalBoard(state)
        converted_action = state_ob.convert_action_to_optimal(action)
        converted_state = self.convert_state(state_ob.optimal_board)
        next_ob = OptimalBoard(next_state)
        converted_next_state = self.convert_state(next_ob.optimal_board)

        self.network.add_train_set(converted_state,
                                   converted_action,
                                   reward,
                                   converted_next_state,
                                   done)

    def _episode_feedback(self, reward):
        # To reduce no of fitting times
        self.network.study()
