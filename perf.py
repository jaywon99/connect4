import time

from boardAI import Arena, PlayerMode
from connect4 import Connect4Board
from players import load_player

def play():
    board = Connect4Board()
    start = time.process_time()
    # player1 = load_player(name="RandomPlayer1",
    #                       storage="models/random_playerX", cls="RandomPlayer")
    player1 = load_player(name="RandomPlusPlayer1",
                        storage="models/randomplus_playerX", cls="RandomPlusPlayer")
    # player1 = load_player(name="PTablePlayer1",
    #                       storage="models/ptable_playerX", cls='PredictionTablePlayer')
    # player1 = load_player(
    #     name="QPlayerX", storage="models/q_playerX", cls="QLearningPlayer")
    # player1 = load_player(name="DQNPlayerX", storage="models/dqn_playerX",
    #                       cls="DQNPlayer", network_storage='./models/dqn1.ckpt')
    # player1 = load_player(name="DDQNPlayerX", storage="models/ddqn_playerX",
    #                       cls="DDQNPlayer", network_storage='./models/ddqn1.ckpt')
    # player1 = load_player(
    #     name="Human1", storage="models/human_player1", cls="HumanPlayer")
    # player1 = load_player(name="NegamaxPlayer1",
    #                       storage="models/negamax_player1", cls="NegamaxPlayer")
    # player1 = load_player(name="AlphaBetaNegamaxPlayer1",
    #                       storage="models/ab_negamax_player1", cls="AlphaBetaNegamaxPlayer")
    # player1 = load_player(name="MCTSRandomPlayer1",
    #                       storage="models/mcts_random_player1", cls="MCTSRandomPlayer")
    end = time.process_time()
    print("Load P1", end-start)
    start = end
    # player2 = load_player(name="RandomPlayer2",
    #                       storage="models/random_player2", cls="RandomPlayer")
    # player2 = load_player(name="RandomPlusPlayer2",
    #                       storage="models/randomplus_player2", cls="RandomPlusPlayer")
    # player2 = load_player(name="PTablePlayer2",
    #                       storage="models/ptable_player2", cls='PredictionTablePlayer')
    # player2 = load_player(
    #     name="QPlayer2", storage="models/q_player2", cls="QLearningPlayer")
    # player2 = load_player(name="DQNPlayer2", storage="models/dqn_player2",
    #                       cls="DQNPlayer", network_storage='./models/dqn2.ckpt')
    # player2 = load_player(name="DDQNPlayer2", storage="models/ddqn_player2",
    #                       cls="DDQNPlayer", network_storage='./models/ddqn2.ckpt')
    # player2 = load_player(
    #     name="Human2", storage="models/human_player2", cls="HumanPlayer")
    # player2 = load_player(name="NegamaxPlayer2",
    #                       storage="models/negamax_player2", cls="NegamaxPlayer")
    player2 = load_player(name="AlphaBetaNegamaxPlayer2",
                        storage="models/ab_negamax_player2", cls="AlphaBetaNegamaxPlayer")
    # player2 = load_player(name="MCTSRandomPlayer2",
    #                       storage="models/mcts_random_player2", cls="MCTSRandomPlayer")
    end = time.process_time()
    print("Load P2", end-start)
    start = end

    arena_train = Arena(board, [player1, player2], mode=PlayerMode.TRAIN)
    arena_play = Arena(board, [player1, player2], mode=PlayerMode.PLAY)

    # arena_train.reset()
    # arena_train.duel(render='human')

    arena_play.reset()
    arena_play.duel(render='human')
    print(arena_play.results, player1.elo, player2.elo)

    # print(player1.elo, player2.elo)
    # for _ in range(100):
    #     start = time.process_time()
    #     for i in range(10):
    #         arena_train.reset()
    #         arena_train.duel(render=None)
    #         end = time.process_time()
    #         print("Study", end-start)
    #         start = end

    #     arena_play.reset_results()
    #     for i in range(10):
    #         arena_play.reset()
    #         arena_play.duel(render=None)
    #         end = time.process_time()
    #         print("Play", end-start)
    #         start = end
    #     print(arena_play.results, player1.elo, player2.elo)

    #     player1.save()
    #     end = time.process_time()
    #     print("Save1", end-start)
    #     start = end
    #     player2.save()
    #     end = time.process_time()
    #     print("Save2", end-start)
    #     start = end

from cProfile import Profile
from pstats import Stats

profiler = Profile()
profiler.runcall(play)
stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()