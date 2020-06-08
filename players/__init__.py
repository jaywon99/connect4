
from boardAI import RandomPlayer
from .ptable import PredictionTablePlayer
from .qlearning import QLearningPlayer
from .human import HumanPlayer
from .dqn import DQNPlayer
from .ddqn import DDQNPlayer
from .minimax import NegamaxPlayer, AlphaBetaNegamaxPlayer, AlphaBetaNegamaxRandomPlayer
from .mcts import MCTSRandomPlayer
from .randomplus import RandomPlusPlayer

def load_player(name=None, storage=None, cls=None, *args, **kwargs):
    if cls == 'HumanPlayer':
        return HumanPlayer(name=name, storage=storage, *args, **kwargs)
    if cls == 'RandomPlayer':
        return RandomPlayer(name=name, storage=storage, *args, **kwargs)
    if cls == 'RandomPlusPlayer':
        return RandomPlusPlayer(name=name, storage=storage, *args, **kwargs)
    if cls == 'PredictionTablePlayer':
        return PredictionTablePlayer(name=name, storage=storage, *args, **kwargs)
    if cls == 'QLearningPlayer':
        return QLearningPlayer(name=name, storage=storage, *args, **kwargs)
    if cls == 'DQNPlayer':
        # egreedy=0.2, hidden_layers=[54, 54], learing_rate=0.001, network_storage=None
        return DQNPlayer(name=name, storage=storage, *args, **kwargs)
    if cls == 'DDQNPlayer':
        # egreedy=0.2, hidden_layers=[54, 54], learing_rate=0.001, network_storage=None
        return DDQNPlayer(name=name, storage=storage, *args, **kwargs)
    if cls == 'NegamaxPlayer':
        return NegamaxPlayer(name=name, storage=storage, *args, **kwargs)
    if cls == 'AlphaBetaNegamaxPlayer':
        # return AlphaBetaNegamaxPlayer(name=name, storage=storage, *args, **kwargs)
        return AlphaBetaNegamaxRandomPlayer(name=name, storage=storage, *args, **kwargs)
    if cls == 'MCTSRandomPlayer':
        return MCTSRandomPlayer(name=name, storage=storage, *args, **kwargs)
        
    raise NotImplementedError