from ptable import PredictionTable, learning
from smart_connect4 import *

# PLAYER X FIRST

p_table = PredictionTable(learning_rate=0.5)
p_table.load('p_table.dat')
print("TOTAL", p_table.step, "ROUND PLAYED")
c4 = AutoConnect4(8, 6)
# smart_o = SmartO(p_table)
# smart_x = SmartX(p_table)
# smart_ox = SmartOX(p_table)

MAX=100
STEP=1
# MAX=1000
# STEP=100
last_size = len(p_table.pred_table)
for step in range(0, MAX, STEP):
    s = 0
    for step1 in range(STEP):
        winner = c4.play_game()
        p_table.next_step()
        learning(p_table, c4.history, winner)
        s += len(c4.history)

    p_table.save('p_table.dat')
    print("Step", p_table.step, "Total", len(p_table.pred_table)-last_size, s, "States")
    last_size = len(p_table.pred_table)

'''
    count = {'O': 0, 'X': 0, '=': 0}
    for step1 in range(1000):
        (result_board, winner) = smart_o.play_game()
        count[winner] += 1
    print("STEP", step, "SMART_O", count)

    count = {'O': 0, 'X': 0, '=': 0}
    for step1 in range(1000):
        (result_board, winner) = smart_x.play_game()
        count[winner] += 1
    print("STEP", step, "SMART_X", count)

    (result_board, winner) = smart_ox.play_game()
    print("STEP", step, "SMART_OX", result_board, "WINNER", winner)
    if winner != '=':
        smart_ox.print_board(result_board)
'''


