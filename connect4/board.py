import math

from boardAI import AbstractBoard, GameResult

# TODO: 자료 형식을 정의하자 (1. internal, 2. between player, 3. rendering)

MAX_ROWS = 6
MAX_COLS = 7
# need optimization, make optimized if statement
D = [[( 0, -3), ( 0, -2), ( 0, -1)], # path 1: same row (-3 ~ 0)
    [( 0, -2), ( 0, -1), ( 0, +1)], # path 2: same row (-2 ~ 1)
    [( 0, -1), ( 0, +1), ( 0, +2)], # path 3: same row (-1 ~ 2)
    [( 0, +1), ( 0, +2), ( 0, +3)], # path 4: same row ( 0 ~ 3)
    [(+1,  0), (+2,  0), (+3,  0)], # path 5: same col ( 0 ~ 3) 
    ######### row should be max of same col
    [(-3, -3), (-2, -2), (-1, -1)], # path 6: diagonal (-3, -3 ~ 0,  0)
    [(-2, -2), (-1, -1), (+1, +1)], # path 7: diagonal (-2, -2 ~ 1,  1)
    [(-1, -1), (+1, +1), (+2, +2)], # path 8: diagonal (-1, -1 ~ 2,  2)
    [(+1, +1), (+2, +2), (+3, +3)], # path 9: diagonal ( 0,  0 ~ 3,  3)
    [(-3, +3), (-2, +2), (-1, +1)], # path A: diagonal (-3,  3 ~ 0,  0)
    [(-2, +2), (-1, +1), (+1, -1)], # path B: diagonal (-2,  2 ~ 1, -1)
    [(-1, +1), (+1, -1), (+2, -2)], # path C: diagonal (-1,  1 ~ 2, -2)
    [(+1, -1), (+2, -2), (+3, -3)]] # path D: diagonal ( 0,  0 ~ 3, -3)
        
class Connect4Board(AbstractBoard):
    # Two Player Colors
    ALL_COLORS = {0: ' ', 1: 'O', -1: 'X'}    # 0, 1, -1
    COLORS = ['O', 'X']
    COLOR_TO_INTERNAL = {'O': 1, 'X': -1}

    class Reward:
        WIN = 1
        TIE = 0
        PLAYING = 0
        ERROR = -math.inf

    def __init__(self):
        super().__init__()

    def reset(self):
        super().reset()
        # 0 means EMPTY, 1 means Player #1, -1 means Player #2
        #  0  1  2  3  4  5  6
        #  7  8  9 10 11 12 13
        # 14 15 16 17 18 19 20
        # 21 22 23 24 25 26 27
        # 28 29 30 31 32 33 34
        # 35 36 37 38 39 40 41
        self._board = [0] * (6*7)  # total 6 rows 7 columns board
        self._n_turn = 0

    def get_colors(self):
        return Connect4Board.COLORS

    @property
    def n_turn(self):
        return self._n_turn

    def _render_for_human(self):
        print('+---+---+---+---+---+---+---+')
        for row in range(0, MAX_ROWS*MAX_COLS, MAX_COLS):
            print('|', end='')
            for idx in range(row, row + MAX_COLS):
                print(
                    '', Connect4Board.ALL_COLORS[self._board[idx]], '|', end='')
            print('')
            print('+---+---+---+---+---+---+---+')
        print('-------------------------------')

    def render(self, mode='human'):
        ''' display board '''
        if mode == 'human':
            return self._render_for_human()
        # if mode == 'network' or etc
        return

    def is_possible_action(self, action):
        return self._board[action] == 0  # 최상단이 비어있으면 둘 수 있다.

    def get_availables(self):
        # 최 상단이 비어있으면 둘 수 있다!
        return [i for i in range(MAX_COLS) if self._board[i] == 0]

    def drop_stone(self, col, color):
        for pos in reversed(range(col, col+MAX_ROWS*MAX_COLS, MAX_COLS)):
            if self._board[pos] == 0:
                self._board[pos] = color
                return pos, pos // MAX_COLS  # 여기를 써야 할지.. 아니면 컨버젼을 해야 할지

        raise "Unavailable Action"

    def get_status(self, color):
        ''' return status by color and available actions. if cell in board == 0, it's available. '''
        return self.to_status(color), self.get_availables()

    def play(self, action, color):
        ''' play action and get result.
        reward (if possible, depend on game), result (GameResult - PLAY_NEXT, PLAY_AGAIN, END_WIN, END_TIE, END_ERROR)
        '''
        if self.end:
            # SHOULD NOT BE HERE! EXCEPTION vs ERROR MESSAGE vs LOOSE MESSAGE
            return Connect4Board.Reward.ERROR, GameResult.END, None

        if not self.is_possible_action(action):
            # SHOULD NOT BE HERE! EXCEPTION vs ERROR MESSAGE vs LOOSE MESSAGE
            # status, reward (-math.inf), END
            return Connect4Board.Reward.ERROR, GameResult.END, None

        self._n_turn += 1
        _color = Connect4Board.COLOR_TO_INTERNAL[color]
        pos, row = self.drop_stone(action, _color)
        won = self._win(action, row, _color)

        if won:
            self.end = True
            return Connect4Board.Reward.WIN, GameResult.END, None

        if 0 in self._board:  # still place to put stone
            # We don't know score yet.
            return Connect4Board.Reward.PLAYING, GameResult.PLAY_NEXT, None

        self.end = True
        return Connect4Board.Reward.TIE, GameResult.END, None

    def is_winning_move(self, action, color):
        if self.end:
            return False

        if not self.is_possible_action(action):
            return False

        _color = Connect4Board.COLOR_TO_INTERNAL[color]
        pos, row = self.drop_stone(action, _color)
        won = self._win(action, row, _color)
        self._board[pos] = 0
        return result

    def _win(self, col, row, color):
        ''' evaluate board and return result
        '''
        for d in D:
            for (r, c) in d:
                if row+r < 0 or row+r >= MAX_ROWS or col+c < 0 or col+c >= MAX_COLS:
                    break
                if self._board[(row+r)*MAX_COLS + col+c] != color:
                    break
            else:
                # print(row, col, d)
                return True

        return False

    def to_status(self, color):
        # TODO: color 입장에서 board를 다시 보여주기 (어떻게???)
        return self._board[:]
