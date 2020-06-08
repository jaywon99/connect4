import pickle

class TranspositionTable:
    EXACT = 0
    LOWERBOUND = 1
    UPPERBOUND = 2

    def __init__(self):
        self.table = {}
        self.tree = StateTree()

    def put(self, state, depth, flag, value, actions):
        # depth, flag, value, actions
        self.table[state] = (depth, flag, value, actions)

    def get(self, state):
        if state in self.table:
            return self.table[state]
        return None

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.table = pickle.load(f)
        except:
            self.table = {}
        print("Table loaded")
        pass

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.table, f)
        print("Table saved")

class StateTree:
    def __init__(self):
        self.tree = {}

    def set_child(self, parent, action, child):
        if parent not in self.tree:
            self.tree[parent] = {}
        self.tree[parent][action] = child

    def get_children(self, parent):
        return self.tree[parent]

