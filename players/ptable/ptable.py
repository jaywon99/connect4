import pickle

# 문제1: 총 623529개의 case가 존재
# 이것을 O/X/ 의 9개짜리로 변경

class PredictionTable:
    def __init__(self, learning_rate = 0.1):
        self.pred_table = {}
        self.learning_rate = learning_rate
        self.step = 0

    def lookup(self, board_id):
        if board_id not in self.pred_table:
            self.pred_table[board_id] = [0.0] * 9
        return self.pred_table[board_id]

    def learn(self, board_id, pos, next_predict):
        if board_id not in self.pred_table:
            self.pred_table[board_id] = [0.0] * 9

        p = self.pred_table[board_id][pos]
        next_predict = p + self.learning_rate * (next_predict - p)
        # print("UPDATE PRED_TABLE", board_id, "FROM", p, "TO", next_predict)
        self.pred_table[board_id][pos] = next_predict
        return next_predict

    def set(self, board_id, pos, value):
        if board_id not in self.pred_table:
            self.pred_table[board_id] = [0.0] * 9

        # print("SET PRED_TABLE", board_id, value)
        self.pred_table[board_id][pos] = value
        return value

    def next_step(self):
        self.step += 1
        self.learning_rate *= 0.99

    def serialize(self):
        return pickle.dumps((self.step, self.learning_rate, self.pred_table))

    def deserialize(self, obj):
        if obj == None:
            self.pred_table = {}
            # self.learning_rate = learning_rate
            self.step = 0
        else:
            self.step, self.learing_rate, self.pred_table = pickle.loads(obj)

