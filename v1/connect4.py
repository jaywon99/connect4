import random

# Connect4 Board
# 8 holes (0th to 7th) and 6 depth
# Red play first

class Connect4Board:
    def __init__(self, holes=8, depth=6):
        self.holes = holes
        self.depth = depth
        self.init_board()

    def init_board(self):
        self.seq = ''
        self.board = [[] for i in range(self.holes)]
        self.history = [self.board_to_map()]

    def get_candidates(self):
        candidates = []
        for h in range(self.holes):
            if len(self.board[h]) < self.depth:
                candidates.append(h)
        return candidates

    def board_to_map(self):
        maps = [''] * self.holes
        for hole in range(self.holes):
            x1 = r''.join(self.board[hole])+' '*self.depth
            x2 = x1[:self.depth]
            maps[hole] = x2[::-1]
        return maps

    def is_win(self):
        candidates = self.get_candidates()
        if len(candidates) == 0:
            return '='

        maps = self.board_to_map()
        last_hole = int(self.seq[-1])
        last_depth = self.depth - len(self.board[last_hole]) 
        last_color = maps[last_hole][last_depth]

        # print(last_hole, last_depth)

        # check below
        if last_depth + 3 < self.depth:
            if last_color == maps[last_hole][last_depth+1] and \
               last_color == maps[last_hole][last_depth+2] and \
               last_color == maps[last_hole][last_depth+3]:
                   # print("WIN", "|", 4, last_color)
                   return last_color

        # check left - horizontal
        cnt = 1
        for step in range(1, self.holes):
            if last_hole + step >= self.holes:
                break
            if last_color == maps[last_hole+step][last_depth]:
                cnt += 1
            else:
                break
        for step in range(1, self.holes):
            if last_hole - step < 0:
                break
            if last_color == maps[last_hole-step][last_depth]:
                cnt += 1
            else:
                break
        if cnt >= 4:
            # print("WIN", "-", cnt, last_color)
            return last_color

        # check \ diagonal
        cnt = 1
        for step in range(1, self.holes):
            if last_hole + step >= self.holes:
                break
            if last_depth + step >= self.depth:
                break
            if last_color == maps[last_hole+step][last_depth+step]:
                cnt += 1
            else:
                break
        for step in range(1, self.holes):
            if last_hole - step < 0:
                break
            if last_depth - step < 0:
                break
            if last_color == maps[last_hole-step][last_depth-step]:
                cnt += 1
            else:
                break
        if cnt >= 4:
            # print("WIN", r'\\', cnt, last_color)
            return last_color

        # check / diagonal
        cnt = 1
        for step in range(1, self.holes):
            if last_hole + step >= self.holes:
                break
            if last_depth - step < 0:
                break
            if last_color == maps[last_hole+step][last_depth-step]:
                # print("SAME", maps[last_hole+step][last_depth-step], last_hole+step, last_depth-step)
                cnt += 1
            else:
                break
        for step in range(1, self.holes):
            if last_hole - step < 0:
                break
            if last_depth + step >= self.depth:
                break
            if last_color == maps[last_hole-step][last_depth+step]:
                # print("SAME", maps[last_hole-step][last_depth+step], last_hole-step, last_depth+step)
                cnt += 1
            else:
                break
        if cnt >= 4:
            # print("WIN", r'/', cnt, last_color)
            return last_color

        return ' '

    def print_board(self):
        maps = self.board_to_map()

        print('---+---+---+---+---+---+---+---')
        for y in range(0, self.depth):
            for x in range(0, self.holes):
                print('', maps[x][y], '|', end='')
            print('')
            print('---+---+---+---+---+---+---+---')
        print('--------------------------------------------')

    def put_stone(self, holes, color):
        # print("PLAY", color, holes)
        self.board[holes].append(color)
        self.seq += str(holes)
        self.history.append(self.board_to_map())

    def try_stone(self, holes, color):
        self.board[holes].append(color)
        maps = self.board_to_map()
        self.board[holes][:-1]
        return maps
