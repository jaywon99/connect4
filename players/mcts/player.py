''' implement negamax algorithm '''

import random
import math
from collections import defaultdict

import pickle

from boardAI import AbstractPlayer, GameResult
from connect4 import OptimalBoard, Connect4Board
from connect4.selfplay import SelfPlayConnect4Board as SP

class MCTSRandomPlayer(AbstractPlayer):
    ''' monte carlo tree search algoritm '''
    DEPTH = 10

    @staticmethod
    def _default_stats():
        ''' to use pickle, required to declare to method instead of lambda '''
        return [0, 1e-4]

    def __init__(self, simulations=1, C=1/math.sqrt(2), *args, **kwargs):
        self.simulations = int(simulations)
        self.C = float(C)
        self._stats = defaultdict(MCTSRandomPlayer._default_stats)
        self.DEBUG = False
        print(self.C, self.simulations)
        super().__init__(*args, **kwargs)

    def serialize(self):
        return pickle.dumps(self._stats)

    def deserialize(self, obj):
        if obj != None:
            self._stats = pickle.loads(obj)

    @staticmethod
    def to_board_id(board):
        ''' board id to make node '''
        return OptimalBoard(board).board_id
        # return OptimalBoard.board_to_id(board)

    def _choose(self, state, available_actions):
        # return smart_turn(self.env)
        my_color = Connect4Board.COLOR_TO_INTERNAL[self.color]
        stats, depth = self.search(state, my_color, self.simulations, self.C)
        return self.select_best_move(stats, depth, state, my_color)

    def search(self, board, start_color, simulations, C):
        ''' implement monte carlo tree search algorithm
        '''
        # CHECK LEAF NODE / DO NOT NEED TO CHECK DEPTH = 0 BECASE Connect4 is too small
        # LEAF NODE is checked on play time

        stats = self._stats
        root = board
        max_depth = 0

        for _ in range(simulations):
            node = root[:]
            states = []

            # select leaf node
            depth = 0
            done = False
            color = start_color
            while not done:
                depth += 1
                action, select = self.select_next_move(stats, node, color, C)

                reward, done = SP.play(node, action, color)
                color = SP.next(color)

                states.append(MCTSRandomPlayer.to_board_id(node))

                if not select:
                    break

            max_depth = max(depth, max_depth)

            # run simulation if not at the end of the game tree
            if not done:
                result = self.simulate(node, start_color) # TODO: 여기를 어떻게 할지
            else:
                if reward == 0:
                    result = 0.5
                else:
                    result = 0

            # propagate results
            for state in reversed(states):
                result = 1 - result
                stats[state][0] += 1
                stats[state][1] += result

        return stats, max_depth

    def select_next_move(self, stats, board, color, C):
        """Select the next state and consider if it should be expanded (UCT)"""

        bestscore = None
        bestmove = None

        # my_id = MCTSRandomPlayer.to_board_id(board)

        children = []
        for action in SP.available_actions(board):
            # clone and play mode - can be play and rollback mode
            next_board = board[:]
            SP.play(next_board, action, color)
            children.append((action, stats[MCTSRandomPlayer.to_board_id(next_board)]))

        total_n = sum(x[0] for (_, x) in children)

        for child_move, child_stat in children:
            n, w = child_stat
            if n == 0: # 한번도 안가봤으면 가보자!
                return child_move, False
            else: # 승률이 높고 (exploitation), 가장 적게 가본 곳이 좋은 곳 (exploration)
                score = (w / n) + C * math.sqrt(2 * math.log(total_n) / n)
                # if my_id == 70645:
                #     print("CHECK IN ", my_id, child_move, w, n, score, bestscore, next_id)
                # if next_id == 119797:
                #     print("JUMP IN ", my_id, child_move, w, n, score, bestscore, next_id)
                if bestscore is None or score > bestscore:
                    bestscore = score
                    bestmove = child_move

        # if my_id == 70645:
        #     print("SELECTED", bestmove, bestscore)

        assert bestmove is not None
        return bestmove, True        

    def select_best_move(self, stats, depth, board, color):
        """Select the best move at the end of the Monte Carlo tree search"""

        bestscore = -1
        bestmove = None
        total_n = 0

        for action in SP.available_actions(board):
            next_board = board[:]
            SP.play(next_board, action, color)
            n, w = stats[MCTSRandomPlayer.to_board_id(next_board)]
            if n == 0:
                continue
            total_n += n
            if self.DEBUG: print('Move %d score: %d/%d (%0.1f%%)' % (action, w, n, w/n*100))
            score = w/n
            if score > bestscore or (score == bestscore and random.random() <= 0.5): # 가장 많이 방문해 본 길을 따라 간다. WHY???
                bestmove = action
                bestscore = score

        assert bestmove is not None

        if self.DEBUG: print('Maximum depth: %d, Total simulations: %d on %d' % (depth, total_n, MCTSRandomPlayer.to_board_id(board)))

        return bestmove

    def simulate(self, board, start_color):
        # random simulator ( Light playouts )
        node = board[:]
        done = False
        color = start_color
        while not done:
            actions = SP.available_actions(node)

            reward, done = SP.play(node, random.choice(actions), color)
            color = SP.next(color)

        if reward == 0: # TIE
            return 0.5
        elif color == start_color:
            return 1
        else:
            return 0
