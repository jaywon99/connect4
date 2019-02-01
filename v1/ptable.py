import pickle
import connect4

# 문제1: 총 623529개의 case가 존재
# 이것을 O/X/ 의 9개짜리로 변경

class PredictionTable:
    def __init__(self, learning_rate = 0.1):
        self.pred_table = {}
        self.learning_rate = learning_rate
        self.step = 0

    def lookup(self, state):
        if state not in self.pred_table:
            self.pred_table[state] = 0.5
        return self.pred_table[state]

    def learn(self, state, next_predict):
        p = 0.5 if state not in self.pred_table else self.pred_table[state]
        next_predict = p + self.learning_rate * (next_predict - p)
        self.pred_table[state] = next_predict
        return next_predict

    def set(self, state, value):
        self.pred_table[state] = value
        return value

    def next_step(self):
        self.step += 1

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.step, self.learning_rate, self.pred_table), f)

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.step, self.learing_rate, self.pred_table = pickle.load(f)
        except:
            self.pred_table = {}
            # self.learning_rate = learning_rate
            self.step = 0

def learning(p_table, history, winner):
    # for winner
    board_winner = history[::-2]
    np = 1.0 if winner != '=' else 0.5
    p_table.set(''.join(board_winner[0]), np)
    # print("RESULT", board_winner, np)
    for winner in board_winner[1:]:
        np = p_table.learn(''.join(winner), np)
        # print("LEARN", board_winner, np)
        # print(board_winner, p, np)

    board_looser = history[-2::-2]
    np = 0.0 if winner != '=' else 0.5
    p_table.set(''.join(board_looser[0]), np)
    # print("RESULT", board_looser, np)
    for looser in board_looser[1:]:
        np = p_table.learn(''.join(looser), np)
        # print("LEARN", board_looser, np)
        # print(board_looser, p, np)

    # print("LEARNED------------")
