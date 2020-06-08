from enum import Enum

class PlayerMode(Enum):
    # player mode
    TRAIN = 0
    PLAY = 1

class GameResult(Enum):
    # game result
    PLAY_NEXT = 1
    PLAY_AGAIN = 2
    # END = -1
    END = -1
    END_ERROR = -2
