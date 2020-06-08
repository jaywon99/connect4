
def board_to_id(board):
    _id = 0
    for digit in (board):
        _id = (_id << 2) | (digit & 3)
    return _id

# TOTAL 8 converion way
CONVERSIONS = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8], # -
    [0, 3, 6, 1, 4, 7, 2, 5, 8], # >y  (rotate 90 and flip y)
    [2, 1, 0, 5, 4, 3, 8, 7, 6], # y   (flip y)
    [2, 5, 8, 1, 4, 7, 0, 3, 6], # >>> (rotate 90 3 times)
    [6, 3, 0, 7, 4, 1, 8, 5, 2], # >   (rotate 90 1 time)
    [6, 7, 8, 3, 4, 5, 0, 1, 2], # >>y (rotate 90 2 times and flip y)
    [8, 5, 2, 7, 4, 1, 6, 3, 0], # >>>y (rotate 90 3 times and flip y)
    [8, 7, 6, 5, 4, 3, 2, 1, 0]  # >>  (rotate 90 2 times)
]

class OptimalBoard:
    def __init__(self, board):
        self.idx = -1
        self.board_id = 100000000
        for idx, C in enumerate(CONVERSIONS):
            y = [0] * 9
            for i, v in enumerate(board):
                y[C[i]] = v
            _id = board_to_id(y)
            if _id < self.board_id:
                self.board_id = _id
                self.idx = idx

    def get_board_id(self):
        self.board_id

    def convert_available_actions(self, available_actions):
        C = CONVERSIONS[self.idx]
        return [C[action] for action in available_actions]

    def convert_action(self, action):
        C = CONVERSIONS[self.idx]
        for i, v in enumerate(C):
            if v == action:
                return i
        assert 0 == 1



def rotate90(board):
    C = [2, 5, 8, 1, 4, 7, 0, 3, 6]
    y = [0] * 9
    for i, v in enumerate(board):
        y[C[i]] = v
    return y

def flip_y(board):
    C = [2, 1, 0, 5, 4, 3, 8, 7, 6]
    y = [0] * 9
    for i, v in enumerate(board):
        y[C[i]] = v
    return y

def flip_x(board):
    C = [6, 7, 8, 3, 4, 5, 0, 1, 2]
    y = [0] * 9
    for i, v in enumerate(board):
        y[C[i]] = v
    return y

def flip_diagonal1(board):
    C = [0, 3, 6, 1, 4, 7, 2, 5, 8]
    y = [0] * 9
    for i, v in enumerate(board):
        y[C[i]] = v
    return y

def flip_diagonal2(board):
    C = [8, 5, 2, 7, 4, 1, 6, 3, 0]
    y = [0] * 9
    for i, v in enumerate(board):
        y[C[i]] = v
    return y

x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
y = x
print(y, "-")
print(flip_y(y), "y")
print(flip_x(y), "x")
print(flip_diagonal1(y), "1")
print(flip_diagonal2(y), "2")
y = rotate90(y)
print(y, ">")
print(flip_y(y), ">y")
print(flip_x(y), ">x")
print(flip_diagonal1(y), ">1")
print(flip_diagonal2(y), ">2")
y = rotate90(y)
print(y, ">>")
print(flip_y(y), ">>y")
print(flip_x(y), ">>x")
print(flip_diagonal1(y), ">>1")
print(flip_diagonal2(y), ">>2")
y = rotate90(y)
print(y, ">>>")
print(flip_y(y), ">>>y")
print(flip_x(y), ">>>x")
print(flip_diagonal1(y), ">>>1")
print(flip_diagonal2(y), ">>>2")
