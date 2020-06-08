''' qlearning agent '''
import random
import pickle

from boardAI import AbstractPlayer
from connect4 import Connect4Board
from connect4.selfplay import SelfPlayConnect4Board as SP

class RandomPlusPlayer(AbstractPlayer):
    ''' random player, but in winning move, play first. '''
    def _choose(self, state, available_actions):
        my_color = Connect4Board.COLOR_TO_INTERNAL[self.color]
        for action in available_actions:
            if SP.winning_move(state, action, my_color):
                # is this my winning move?
                return action
        opposite_color = SP.next(my_color)
        for action in available_actions:
            if SP.winning_move(state, action, opposite_color):
                # is this opposite winning move?
                return action
        return random.choice(available_actions)
