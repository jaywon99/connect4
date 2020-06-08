# Tic-Tac-Toe v1

Self Playing을 통한 Tic-Tac-Toe 배우기

Tic-Tac-Toe는 Depth가 최대 9밖에 안되므로, full-depth를 학습시킴.

학습자료 및 p value의 convergence는https://users.auth.gr/kehagiat/Research/GameTheory/12CombBiblio/TicTacToe.pdf 을 참조

RAW자료는 self-play를 통해 만듬 (위의 pdf는 모든 case를 다 만듬)


## p_table_v1.py
위의 pdf는 state를 최소화 하였으나, 본 경우에는 원래대로 진행하며, 현재 5478건이 만들어짐.

## p_table_v2.py


## Prediction Table을 보고 싶으면
```python
from ptable import PredictionTable
p_table = PredictionTable(learning_rate=0.5)
p_table.load('p_table.dat')
```

