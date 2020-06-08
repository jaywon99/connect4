import pickle
from connect4.selfplay import SimpleConnect4Board as SC4

def navigate(tp, b, color, depth):
    if depth >= 10:
        return
    for action in b.available_actions():
        next_b = b.clone()
        result, done = next_b.play(action, color)
        if not done:
            if next_b.to_id() not in tp:
                pass
            else:
                print(' '*(depth*2), 'FROM', b.to_id(), 'ACTION', action, 'ID', next_b.to_id(), end=' ')
                print('VISITED', tp[next_b.to_id()])
                navigate(tp, next_b, -color, depth+1)
        else:
            print(' '*(depth*2), 'FROM', b.to_id(), 'ACTION', action, 'ID', next_b.to_id(), end=' ')
            print('WIN', result)

with open('models/ab_negamax_player2', 'rb') as f: 
    obj = pickle.load(f)
    tp = obj[2]

b = SC4(board=[0]*42)
navigate(tp, b, 1, 0)
