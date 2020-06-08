from boardAI import AbstractPlayer
from connect4 import OptimalBoard, Connect4Board

class WrongMoveError(Exception):
    pass

MAX_ROWS = 6
MAX_COLS = 7
class HumanPlayer(AbstractPlayer):
    ''' random player '''
    def _choose(self, state, available_actions):

        self.render_for_human(state)
        while True:
            try:
                move = int(input('Your move: ')) - 1
                if move not in available_actions:
                    raise WrongMoveError('available only '+','.join([str(i) for i in available_actions]))
            except ValueError:
                print('Wrong move! Must be an integer between 1-9.')
            except WrongMoveError as e:
                print(e)
            else:
                break

        return move

    def render_for_human(self, board):
        print('+---+---+---+---+---+---+---+')
        for row in range(0, MAX_ROWS*MAX_COLS, MAX_COLS):
            print('|', end='')
            for idx in range(row, row + MAX_COLS):
                print(
                    '', Connect4Board.ALL_COLORS[board[idx]], '|', end='')
            print('')
            print('+---+---+---+---+---+---+---+')
        print('-------------------------------')
