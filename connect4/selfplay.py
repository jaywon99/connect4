from .board import Connect4Board

MAX_ROWS = 6
MAX_COLS = 7
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

# D1 = [[( 0, -3), ( 0, -2), ( 0, -1), (0, +1), (0, +2), (0, +3)], # path 1: same row (-3 ~ 0)
#     [(+1,  0), (+2,  0), (+3,  0)], # path 5: same col ( 0 ~ 3) 
#     ######### row should be max of same col
#     [(-3, -3), (-2, -2), (-1, -1), (+1, +1), (+2, +2), (+3, +3)], # path 6: diagonal (-3, -3 ~ 0,  0)
#     [(-3, +3), (-2, +2), (-1, +1), (+1, -1), (+2, -2), (+3, -3)]] # path A: diagonal (-3,  3 ~ 0,  0)

# TODO: SelfPlay와 Connect4Board를 합칠 방법을 찾아보자!
# TODO(jaywon99): 만들어 넣자!
class SelfPlayConnect4Board:
    @staticmethod
    def drop_stone(board, col, color):
        for pos in reversed(range(col, col+MAX_ROWS*MAX_COLS, MAX_COLS)):  # 계산 vs ARRAY - 큰 차이 없음
            if board[pos] == 0:
                board[pos] = color
                return pos, pos // MAX_COLS  # 여기를 써야 할지.. 아니면 컨버젼을 해야 할지

        raise "Unavailable Action"

    @staticmethod
    def play(board, col, color):
        pos, row = SelfPlayConnect4Board.drop_stone(board, col, color)
        reward = SelfPlayConnect4Board.check_win(board, col, row, color)
        space_left = board.count(0)

        if reward:  # WIN
            return space_left+1, True
        elif space_left == 0:  # TIE
            return space_left, True
        else:  # PLAYING
            return 0, False 

    @staticmethod
    def winning_move(board, col, color):
        pos, row = SelfPlayConnect4Board.drop_stone(board, col, color)  # row를 위해 호출 필요
        reward = SelfPlayConnect4Board.check_win(board, col, row, color)
        board[pos] = 0
        return reward

    @staticmethod
    def available_actions(board):
        return [i for i in range(MAX_COLS) if board[i] == 0]

    @staticmethod
    def next(color):
        return -color

    @staticmethod
    def check_win(board, col, row, color):
        ''' evaluate board and return result
        '''
        for d in D:
            for (r, c) in d:
                if row+r < 0 or row+r >= MAX_ROWS or col+c < 0 or col+c >= MAX_COLS:
                    break
                if board[(row+r)*MAX_COLS + col+c] != color:
                    break
            else:
                # print(row, col, d)
                return True

        return False            

    # @staticmethod
    # def check_win(board, col, row, color):
    #     ''' evaluate board and return result
    #     '''
    #     for d in D1:
    #         cnt = 0
    #         for (r, c) in d:
    #             if row+r < 0 or row+r >= MAX_ROWS or col+c < 0 or col+c >= MAX_COLS:
    #                 cnt = 0
    #             elif board[(row+r)*MAX_COLS + col+c] != color:
    #                 cnt = 0
    #             else:
    #                 cnt += 1
    #                 if cnt >= 3:
    #                     return True

    #     return False            


class SimpleConnect4Board:
    def __init__(self, board=None, parent=None):
        if board is not None:
            # build from board
            self._board = board[:]
            self._left = board.count(0)
            self._next_row = [0] * MAX_COLS
            for i in range(MAX_ROWS*MAX_COLS):
                if self._board[i] == 0:
                    self._next_row[i%MAX_COLS] = i // MAX_COLS
        elif parent is not None:
            # build from parent
            self._board = parent._board[:]
            self._next_row = parent._next_row[:]
            self._left = parent._left
        else:
            raise "board or parent should be passed"

    def available_actions(self):
        # return [i for i, r in enumerate(self._next_row) if r >= 0]
        # return [i for i in range(MAX_COLS) if self._next_row[i] >= 0]  # new trial
        return [i for i in range(MAX_COLS) if self._board[i] == 0] # it is fastest.

    def play(self, col, color):
        # pos, row = SelfPlayConnect4Board.drop_stone(board, col, color)
        row = self._next_row[col]  # find pos
        if row < 0:
            raise "Unavailable Action"

        # drop stone
        # print(row, col, row*MAX_COLS+col, len(self._board))
        self._board[row * MAX_COLS + col] = color
        self._next_row[col] -= 1
        self._left -= 1

        reward = self.check_win(col, row, color)

        if reward:  # WIN
            return self._left+1, True
        elif self._left == 0:  # TIE
            return self._left, True
        else:  # PLAYING
            return 0, False     

    def winning_move(self, col, color):
        row = self._next_row[col]
        if row < 0:
            raise "Unavailable Action"

        reward = self.check_win(col, row, color)

        return reward

    @staticmethod
    def next(color):
        return -color

    def check_win_orig(self, col, row, color):
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

    def check_win(self, col, row, color):
        # vertical
        cnt = 0
        for r in range(row+1, row+4):
            if r >= MAX_ROWS:
                break
            if self._board[r*MAX_COLS+col] != color:
                break
            cnt += 1
        if cnt == 3:
            return True

        # horizontal
        cnt = 0
        for c in range(col-1, col-4, -1):
            if c < 0:
                break
            if self._board[row*MAX_COLS+c] != color:
                break
            cnt += 1
        for c in range(col+1, col+4):
            if c >= MAX_COLS:
                break
            if self._board[row*MAX_COLS+c] != color:
                break
            cnt += 1
        if cnt >= 3:
            return True

        # diagonal \
        cnt = 0
        for t in range(-1, -4, -1):
            if row+t < 0 or row+t >= MAX_ROWS or col+t < 0 or col+t >= MAX_COLS:
                break
            if self._board[(row+t)*MAX_COLS+(col+t)] != color:
                break
            cnt += 1
        for t in range(1, 4):
            if row+t < 0 or row+t >= MAX_ROWS or col+t < 0 or col+t >= MAX_COLS:
                break
            if self._board[(row+t)*MAX_COLS+(col+t)] != color:
                break
            cnt += 1
        if cnt >= 3:
            return True

        # diagonal /
        cnt = 0
        for t in range(-1, -4, -1):
            if row-t < 0 or row-t >= MAX_ROWS or col+t < 0 or col+t >= MAX_COLS:
                break
            if self._board[(row-t)*MAX_COLS+(col+t)] != color:
                break
            cnt += 1
        for t in range(1, 4):
            if row-t < 0 or row-t >= MAX_ROWS or col+t < 0 or col+t >= MAX_COLS:
                break
            if self._board[(row-t)*MAX_COLS+(col+t)] != color:
                break
            cnt += 1
        if cnt >= 3:
            return True

        return False

    BASE64='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    # 이걸 미리 만들어 놓을 수는 없을까?
    def to_id_orig(self):
        # _id = 0
        # for digit in (self._board):
        #     _id = (_id << 2) | (digit & 3)
        # return _id
        hashcode = ''
        for i in range(0, MAX_ROWS*MAX_COLS, 3):
            code = 0
            for j in range(i, i+3):
                code = (code << 2) | self._board[j] & 3
            hashcode += SimpleConnect4Board.BASE64[code]
        return hashcode

    def to_id_latest(self):
        # _id = 0
        # for digit in (self._board):
        #     _id = (_id << 2) | (digit & 3)
        # return _id
        hashcode = ''
        code = 0
        for i,v in enumerate(self._board):
            code = (code << 2) | (v & 3)
            if i % 3 == 2:
                hashcode += SimpleConnect4Board.BASE64[code]
                code = 0
        return hashcode
        
    def to_id(self):
        _id = 0
        for digit in (self._board):
            _id = (_id << 2) | (digit & 3)
        return hex(_id)[2:]  # hex is faster then base64, remove first '0x'
        
    def clone(self):
        return SimpleConnect4Board(parent=self)