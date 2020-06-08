import random

# Connect4 Board
# 7 holes (0th to 7th) and 6 depth
# Red play first

MAX_ROW = 6
MAX_COL = 7

class FlatBoard:
    def __init__(self, data = None):
        self.reset(data)

    def reset(self, data=None):
        if data:
            self.board = data[:]
        else:
            self.board = [0] * (MAX_ROW  * MAX_COL)

    def hash(self):
        h = 0
        for cell in self.board:
            v = cell
            if v == -1: v = 2
            h = (h<<2) + v  # to make short, using h*3 instead of h<<2
        return h

    def __getitem__(self, key):
        (r, c) = key
        return self.board[r*MAX_COL+c]

    def __setitem__(self, key, value):
        (r, c) = key
        self.board[r*MAX_COL+c] = value

    def clone(self):
        return FlatBoard(self.board)

    def score(self):
        return self.board.count(0)

class Connect4:
    PLAY_MORE = 0
    TIE = 1
    WIN = 2

    def __init__(self, source = None):
        if source == None:
            self.board = FlatBoard()
        elif isinstance(source, Connect4):
            self.board = source.board.clone()
        else:
            raise "Source should be Connect4"

    def init_board(self):
        self.seq = []
        self.board.reset()

    def get_available_actions(self):
        candidates = []
        for h in range(MAX_COL):
            if self.board[0, h] == 0:   # 제일 윗칸이 비어있으면 넣을 수 있음
                candidates.append(h)
        return candidates

    def put_stone(self, col, color):
        # print("PLAY", color, col)
        for row in range(MAX_ROW-1, -1, -1):
            if self.board[row, col] == 0: # empty
                self.board[row, col] = color
                win = self.is_win(row, col, color)
                break
        else:
            raise "Unavailable Action"
        # self.seq.append(holes) # WHY DO WE NEED THIS???
        return win

    def is_winning_move(self, col, color):
        # print("PLAY", color, col)
        for row in range(MAX_ROW-1, -1, -1):
            if self.board[row, col] == 0: # empty
                return self.is_win(row, col, color)
        else:
            raise "Unavailable Action"
        
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

    def is_win(self, row, col, color):
        for d in self.D:
            for (r, c) in d:
                if row+r < 0 or row+r >= MAX_ROW or col+c < 0 or col+c >= MAX_COL:
                    break
                if self.board[row+r, col+c] != color:
                    break
            else:
                # print(row, col, d)
                return self.WIN

        for h in range(MAX_COL):
            if self.board[0, h] == 0:   # 제일 윗칸이 비어있으면 넣을 수 있음
                return self.PLAY_MORE # Play more

        return self.TIE # it's TIE!!!

    def score(self):
        return self.board.score()+1

    def get_board_id(self):
        return self.board.hash()

    def print_board(self):
        print('---+---+---+---+---+---+---')
        for row in range(0, MAX_ROW):
            for col in range(0, MAX_COL):
                if self.board[row, col] == 0:
                    c = ' '
                elif self.board[row, col] > 0:
                    c = 'O'
                else:
                    c = 'X'
                print('', c, '|', end='')
            print('')
            print('---+---+---+---+---+---+---')
        print('--------------------------------------------')

