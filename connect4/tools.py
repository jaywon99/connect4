import math

# TODO(jaywon99): 일단은 transparent로 만들고, 혹시 모르니, flap 가능 여부는 확인해보자.
class OptimalBoard:
    # @staticmethod
    # def board_to_id(board):
    #     _id = 0
    #     for digit in (board):
    #         _id = (_id << 2) | (digit & 3)
    #     return _id

    BASE64='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    @staticmethod
    def board_to_id(board):
        # _id = 0
        # for digit in (self._board):
        #     _id = (_id << 2) | (digit & 3)
        # return _id
        hashcode = ''
        for i in range(0, MAX_ROWS*MAX_COLS, 3):
            code = 0
            for j in range(i, i+3):
                code += self._board[j] & 3
            hashcode += OptimalBoard.BASE64[code]
        return hashcode

    def __init__(self, board):
        self._optimized_board = board
        self._board_id = OptimalBoard.board_to_id(board)

    @property
    def board_id(self):
        return self._board_id

    @property
    def optimal_board(self):
        return self._optimized_board

    def convert_action_to_optimal(self, actions):
        return actions

    def convert_action_to_original(self, action):
        return action
