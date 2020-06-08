''' implement negamax algorithm '''

import random
import math

from boardAI import AbstractPlayer, GameResult
from connect4 import OptimalBoard, Connect4Board
from connect4.selfplay import SelfPlayConnect4Board as SP

from .transposition import TranspositionTable

class NegamaxRandomPlayer(AbstractPlayer):
    ''' negamax random tic-tac-toe agent '''
    DEPTH = 10

    def __init__(self, depth=DEPTH, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tp = TranspositionTable()
        self.depth = depth

    def serialize(self):
        return self.tp.serialize()

    def deserialize(self, obj):
        if obj != None:
            self.tp.deserialize(obj)

    def _choose(self, state, available_actions):
        # return smart_turn(self.env)
        # state는 0,1,-1로 이루어진 9칸 array
        # 1. board를 만들 필요가 있을까? 아니면 그냥 state로 동작할까?
        # state, color, available_actions로 negamax를 동작
        # available_actions가 negamax에 필요한가? 그렇지 않음
        my_color = Connect4Board.COLOR_TO_INTERNAL[self.color]
        (_, next_actions) = self.negamax(state, my_color, depth=self.depth)
        return random.choice(next_actions)

    def get_tp(self):
        return self.tp
        
    # TODO(jaywon99): add depth to transition table
    def negamax(self, state, color, depth=DEPTH):
        ''' implement negamax algorithm
        https://en.wikipedia.org/wiki/Negamax
        '''
        # negamax.counter += 1

        # TODO(jaywon99): CHECK LEAF NODE / when DEPTH == 0, WHAT TO DO?
        # LEAF NODE is checked on play time
        if depth == 0:
            return 0, []

        # Transposition Table related work
        # ob = OptimalBoard(state)
        # _id = ob.board_id
        _id = OptimalBoard.board_to_id(state)

        cache = self.tp.get(_id)
        if cache is not None and cache['depth'] > depth:  # TODO(jaywon99): need to check depth is equal?
            return cache['value']

        # RECURSIVE
        actions = SP.available_actions(state)

        # pre-check - find direct winning move and DO IT!
        for action in actions:
            next_color = SP.next(color)
            if SP.winning_move(state, action, color):
                return state.count(0)+1, action

        random.shuffle(actions) # move orders를 쓰면, alpha beta pruning시에 성능이 좋아짐
        best_score = -math.inf
        best_actions = []
        for action in actions:
            next_s = state[:]
            score, done = SP.play(next_s, action, color)
            if not done:
                score, _ = self.negamax(next_s, SP.next(color), depth-1)
                score = -score # negamax

            # pick from all best moves
            if score > best_score:
                best_score = score
                best_actions = [action]
            elif score == best_score:
                best_actions.append(action)

        # case 1: choose random value 1 time
        # choosed_result = random.choice(best_scores)
        # tp.put(_id, choosed_result)
        # return choosed_result

        # case 2: choose random value every time
        self.tp.put(_id, depth=depth, value=(best_score, best_actions))
        return (best_score, best_actions)

