class TranspositionTable:
    def __init__(self):
        self.table = {}

    def get(self, key):
        if key in self.table:
            return self.table[key]
        else:
            return None

    def put(self, key, depth, value):
        self.table[key] = {'depth': depth, 'value': value}

    def serialize(self):
        return self.table

    def deserialize(self, obj):
        if obj != None:
            self.table = obj


class ABPTranspositionTable:  # Alpha-Beta-Pruning Transposition Table
    LOWERBOUND, EXACT, UPPERBOUND = -1, 0, 1

    def __init__(self):
        self.table = {}

    def get(self, key):
        if key in self.table:
            return self.table[key]
        else:
            return None

    def put(self, key, depth, value, flag):
        # if key in self.table and self.table[key]['depth'] < depth:
        #     print("FROM", self.table[key], 'TO', {
        #           'depth': depth, 'value': value, 'flag': flag})
        self.table[key] = {'depth': depth, 'value': value, 'flag': flag}

    def serialize(self):
        return self.table

    def deserialize(self, obj):
        if obj != None:
            self.table = obj
