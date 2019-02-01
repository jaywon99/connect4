import sys
import random

from ptable import PredictionTable 
from smart_connect4 import AutoConnect4

p_table = PredictionTable(learning_rate=0.5)
p_table.load('p_table.dat')
print("TOTAL", p_table.step, "ROUND PLAYED")
c4 = AutoConnect4(8, 6, debug=True)
# board = SmartX(p_table, debug=True)

count = {'R': 0, 'X': 0, '=': 0}
for step in range(1000):
    winner = c4.play_game()
    print("WINNER", winner)
    c4.print_board()
    count[winner] += 1
    if winner == 'O':
        sys.exit(0)

