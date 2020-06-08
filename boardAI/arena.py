import math

from .const import PlayerMode, GameResult
from .board import AbstractBoard


class PlayerList:
    def __init__(self, players, colors):
        assert(len(players) == len(colors))

        self._players = players
        self._pos = 0
        for player, color in zip(players, colors):
            player.color = color

    def next(self):
        self._pos += 1
        if self._pos >= len(self._players):
            self._pos = 0
        return self._players[self._pos]

    def current(self):
        if self._pos < 0:
            raise "Game not played yet"
        return self._players[self._pos]

    def reset(self, mode):
        for player in self._players:
            player.reset()
            player.player_mode = mode
        self._pos = -1

    def __iter__(self):
        return iter(self._players)

    def __len__(self):
        return len(self._players)


class Arena:
    def __init__(self, board: AbstractBoard, players, mode=PlayerMode.TRAIN, K=32):
        self._board = board
        # set colors to player and make list
        self._players = PlayerList(players, board.get_colors())
        self._mode = mode
        self.K = K
        self.reset_results()

    def reset(self):
        self._board.reset()
        self._players.reset(self._mode)

    def reset_results(self):
        self._results = {'TIE': 0}
        for player in self._players:
            self.results[player.name_with_color] = 0

    def duel(self, render=None):
        ''' Play duel.
        render: depend on board, string
        (ex: False = no display, human = "human visible")
        '''
        self.reset()

        done = False
        action = None
        reward = 0
        # history = []

        player = self._players.next()
        while not done:
            self._board.render(render)

            (state, available_actions) = self._board.get_status(player.color)

            if player.is_played():   # is this really required???
                # In board game, feedback is coming after other player played.
                player.feedback(state, reward, False)

            action = player.choose(state, available_actions)
            # print(player.name, action)
            (reward, result, _) = self._board.play(action, player.color)
            # print(reward, result)
            # if recorded:
            #     history.append(action)

            if reward == -math.inf:
                self._board.render(mode='human')
                print("ACTION", action, available_actions, player.name)

            if result == GameResult.PLAY_NEXT:
                player = self._players.next()
            elif result == GameResult.PLAY_AGAIN:
                pass
            else:
                done = True

        self._board.render(render)

        # Calculate ELO
        self._calculate_elo(reward, player)
        if reward == 0:
            self._results['TIE'] += 1
        else:
            self._results[player.name_with_color] += 1

        # FEEDBACK
        self._duel_feedback(reward, player)

        # if recorded:
        #     return (reward, history)
        return reward

    def _duel_feedback(self, reward, winner):
        for each_player in self._players:
            (state, _) = self._board.get_status(each_player.color)
            if reward == 0:
                # reward = 0, done = True
                each_player.feedback(state, reward, True)
                each_player.episode_feedback(reward)
            else:
                if winner == each_player:
                    each_player.feedback(state, reward, True)
                    each_player.episode_feedback(reward)
                else:
                    each_player.feedback(state, -reward, True)
                    each_player.episode_feedback(-reward)

    def _calculate_elo(self, reward, winner):
        ''' calculate ELO logic
        https://en.wikipedia.org/wiki/Elo_rating_system - Mathematical details
        '''

        if self._mode != PlayerMode.PLAY:
            return

        r_sum = 0.0
        r = [0] * len(self._players)
        for idx, each_player in enumerate(self._players):
            r[idx] = 10**(each_player.elo / 400)
            r_sum += r[idx]
        # print(r, r_sum)
        r_prime = [0] * len(self._players)
        for idx, each_player in enumerate(self._players):
            if reward == 0:
                s = 0.5
            elif each_player == winner:
                s = 1
            else:
                s = 0
            e = r[idx] / r_sum
            r_prime = self.K * (s - e)
            # print(idx, s, e, r_prime)
            each_player.elo = each_player.elo + r_prime

    @property
    def results(self):
        return self._results
