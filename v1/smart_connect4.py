import random

from connect4 import Connect4Board
from ptable import PredictionTable 

class AutoConnect4(Connect4Board):
    def __init__(self, holes, depth, **kwargs):
        super().__init__(holes, depth)
        self.debug = kwargs['debug'] if 'debug' in kwargs else False

    def play_random(self, color):
        candidates = self.get_candidates()
        random.shuffle(candidates)
        self.put_stone(candidates[0], color)

    def play_red(self):
        return self.play_random('R')

    def play_white(self):
        return self.play_random('W')

    def play(self):
        if len(self.seq) % 2 == 0:
            self.play_red()
        else:
            self.play_white()
        # if self.debug: self.print_board(next_board)
        # return next_board

    def play_game(self):
        board = self.init_board()
        # print_board(board[-1])
        winner = ' '
        while winner == ' ':
            board = self.play()
            winner = self.is_win()
            if self.debug: self.print_board()
        return winner

class SmartConnect4(AutoConnect4):
    def __init__(self, holes, depth, p_table, **kwargs):
        super().__init__(**kwargs)
        self.p_table = p_table

    def play_smart(self, color):
        candidates = self.get_candidates()
        found_p = -1.0
        found_c = -1
        if self.debug: print("FROM", board)
        for candidate in candidates:
            next_board = board + str(candidate)
            p = self.p_table.lookup(next_board)
            if self.debug: print("CANDIDATE", candidate, p)
            if p > found_p:
                found_p = p
                found_c = candidate
        if self.debug: print("SELECT", found_c, found_p)
        self.put_stone(found_c, color)


class SmartRed(SmartConnect4):
    def play_red(self, board):
        return self.play_smart('R')

class SmartWhite(SmartConnect4):
    def play_white(self, board):
        return self.play_smart('W')

class SmartBoth(SmartConnect4):
    def play_red(self, board):
        return self.play_smart('R')

    def play_white(self, board):
        return self.play_smart('W')

