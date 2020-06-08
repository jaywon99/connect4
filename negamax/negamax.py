import sys
import random
import math
import collections

from connect4 import Connect4
from transposition import TranspositionTable

def negamax(tp, board, player, alpha=-math.inf, beta=math.inf, depth=10):
    if depth == 0:
        return 0, []

    board_id = board.get_board_id()

    orig_alpha = alpha
    orig_depth = depth

    cache = tp.get(board_id)
    if cache and cache[0] > depth:
        # depth, flag, value, actions
        d, flag, value, actions = cache
        if flag == tp.EXACT:
            # if depth == orig_depth: # TODO: ALWAYS TRUE
            #     return value, actions
            return value, actions
        elif flag == tp.LOWERBOUND:
            alpha = max(alpha, value)
        elif flag == tp.UPPERBOUND:
            beta = min(beta, value)

        if alpha >= beta:
            # if depth == orig_depth: # TODO: 도대체 이건 왜하는지.. ㅠㅠ
            #     # game.ai_move = actions
            #     pass
            return value, actions

    negamax.counter += 1

    actions = board.get_available_actions()
    if len(actions) == 0:
        # NO MORE MOVE
        return 0, []        # evaluate current board score

    # To save recursion time (이건 iterative deepening으로 제외할 수 있을 듯)
    for action in actions:
        result = board.is_winning_move(action, player)
        # print(depth, action, result)
        if result == Connect4.TIE:
            # TODO
            tp.put(board_id, depth, tp.EXACT, 0, [action])
            return (0, [action])    # TIE = 0 (means next move is last move)
        if result == Connect4.WIN:
            score = board.score()
            # TODO
            tp.put(board_id, depth, tp.EXACT, score, [action])
            return (score, [action]) # or board.score()-2

    best_score = -math.inf
    best_actions = []

    for action in actions:
        b = Connect4(board)

        result = b.put_stone(action, player)
        score, _ = negamax(tp, b, -player, -beta, -alpha, depth-1)
        score = -score

        if score > best_score:
            best_score = score
            best_actions = [action]
        elif score == best_score:
            best_actions.append(action)

        if alpha < score:
            alpha = score
            # if depth == orig_depth:
            #     # state.ai_move = move
            #     pass
            if alpha > beta:
                break

    if best_score <= orig_alpha:
        flag = tp.UPPERBOUND
    elif best_score >= beta:
        flag = tp.LOWERBOUND
    else:
        flag = tp.EXACT

    tp.put(board_id, depth, flag, best_score, best_actions)
    return best_score, best_actions

board = Connect4()
board.init_board()
done = False

tp = TranspositionTable()
tp.load("table.dat")

played = ''
player = 1
if len(sys.argv) > 1:
    seq = sys.argv[1]
    played += seq
    print("PRE-PLAY", seq)
    for p in seq:
        board.put_stone(int(p), player)
        player = -player
    board.print_board()

negamax.counter = 0

while not done:
    (score, actions) = negamax(tp, board, player, -1, 1, depth=6)
    # print(score, actions, board.get_available_actions())
    action = random.choice(actions)
    # action = actions[0]
    played += str(action)
    result = board.put_stone(action, player)
    print(action, score, actions, played, negamax.counter)
    board.print_board()
    if result != Connect4.PLAY_MORE:
        done = False
        if result == Connect4.TIE:
            print("GAME TIE!!!!")
        else:
            print("PLAYER", player, "WIN and SCORE is", board.score())
        print("COUNTER", negamax.counter)
        break
    player = -player

tp.save("table.dat")


