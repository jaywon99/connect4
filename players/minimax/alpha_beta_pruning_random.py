''' implement negamax algorithm '''

import random
import math

from boardAI import AbstractPlayer, GameResult
from connect4 import OptimalBoard, Connect4Board
# from connect4.selfplay import SelfPlayConnect4Board as SP
from connect4.selfplay import SimpleConnect4Board as SC4

from .transposition import ABPTranspositionTable


class AlphaBetaNegamaxRandomPlayer(AbstractPlayer):
    ''' negamax alpha beta pruning tic-tac-toe agent '''
    DEPTH = 6

    def __init__(self, depth=DEPTH, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tp = ABPTranspositionTable()
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
        sc4 = SC4(board=state)
        # start = time.process_time()
        (_, next_actions) = self.negamax_alpha_beta_pruning(
            sc4, my_color, alpha=-1, beta=1, depth=self.depth)
        # print("ELAPSED", time.process_time()-start)
        # print("FOUND ACTIONS", next_actions, state, _)
        return random.choice(next_actions)

    def get_tp(self):
        return self.tp

    def negamax_alpha_beta_pruning(self, sc4, color, alpha=-math.inf, beta=math.inf, depth=DEPTH):
        ''' implement negamax algorithm with alpha-beta purning
        https://en.wikipedia.org/wiki/Negamax
        '''
        # negamax.counter += 1

        orig_alpha = alpha

        # Transposition Table related work
        # ob = OptimalBoard(state)
        # _id = ob.board_id
        _id = sc4.to_id()
        cache = self.tp.get(_id)
        if cache and cache['depth'] > depth:
            (cached_score, cached_action) = cache['value']
            if cache['flag'] == self.tp.EXACT:
                return (cached_score, cached_action)
            elif cache['flag'] == self.tp.LOWERBOUND:
                alpha = max(alpha, cached_score)
            elif cache['flag'] == self.tp.UPPERBOUND:
                beta = min(beta, cached_score)
            if alpha >= beta:
                return cached_score, cached_action
        # else:
        #     print("MISS", t.seq)

        # CHECK LEAF NODE / DO NOT NEED TO CHECK DEPTH = 0 BECASE Connect4 is too small
        # LEAF NODE is checked on play time
        if depth == 0:
            return 0, []

        # RECURSIVE
        actions = sc4.available_actions()

        # pre-check - find direct winning move and DO IT!
        for action in actions:
            next_color = sc4.next(color)
            if sc4.winning_move(action, color):
                return sc4._left+1, [action]

        # random.shuffle(actions) # move orders를 쓰면, alpha beta pruning시에 성능이 좋아짐
        best_score = -math.inf
        best_actions = []
        for action in actions:
            n_sc4 = sc4.clone()
            score, done = n_sc4.play(action, color)
            if not done:
                score, _ = self.negamax_alpha_beta_pruning(
                    n_sc4, n_sc4.next(color), alpha=-beta, beta=-alpha, depth=depth-1)
                score = -score  # negamax

            # just pick up 1 first best move (random.shuffle make randomness)
            if score > best_score:
                best_score = score
                best_actions = [action]
            elif score == best_score:
                best_actions.append(action)

            if alpha < score:
                alpha = score
                # 결국 alpha = max(alpha, best_score)
                if alpha > beta:
                    break

        if best_score <= orig_alpha:
            flag = self.tp.UPPERBOUND
        elif best_score >= beta:
            flag = self.tp.LOWERBOUND
        else:
            flag = self.tp.EXACT

        self.tp.put(key=_id, depth=depth, value=(
            best_score, best_actions), flag=flag)

        return (alpha, best_actions)
