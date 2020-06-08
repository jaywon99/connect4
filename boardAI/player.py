import random
# import pickle
import msgpack

from .const import PlayerMode


class AbstractPlayer:
    ''' Abstract Agent '''

    HISTORY_STATE = 0
    HISTORY_ACTION = 1
    HISTORY_NEXT_STATE = 2
    HISTORY_REWARD = 3
    HISTORY_DONE = 4

    def __init__(self, name, storage):
        assert(name is not None)
        assert(storage is not None)

        self.history = []
        self._player_mode = PlayerMode.TRAIN
        self._train_mode = False
        self.name = name
        self.storage = storage
        self._elo = 1200
        self.load()

    @property
    def is_train_mode(self):
        return self._train_mode

    @property
    def player_mode(self):
        ''' return True/False if player is train_mode or not '''
        return self._player_mode

    @player_mode.setter
    def player_mode(self, player_mode):
        ''' set train mode (PlayerMode.TRAIN / PlayerMode.PLAY) '''
        self._player_mode = player_mode
        if player_mode == PlayerMode.TRAIN:
            self._train_mode = True
        else:
            self._train_mode = False

    @property
    def name_with_color(self):
        return self.color + '-' + self.name

    def _reset(self):
        ''' reset agent status internal (real class implement this) '''
        pass

    def reset(self):
        ''' reset agent for general purpose.
        It will call _reset internally.
        '''
        self._n_playes += 1
        self.history = []
        self._reset()

    # TODO: is history belongs to player or duel or board
    def is_played(self):
        ''' check start playing '''
        return len(self.history) > 0

    # TODO: is history belongs to player or duel or board
    def save_history(self, state, action):
        ''' to replay, save all history '''
        self.history.append([state, action])

    def pop_history(self):
        ''' backward replay from play book '''
        return self.history.pop()

    def all_history(self):
        ''' get all history from 1st move '''
        return self.history
    # until HERE

    def _choose(self, state, available_actions):
        ''' internal code for next_action '''
        raise NotImplementedError

    def choose(self, state, available_actions):
        ''' call _next_action and save play history
        '''
        action = self._choose(state, available_actions)
        self.save_history(state, action)
        return action

    def _feedback(self, state, action, next_state, reward, done):
        ''' feedback of each play - generally feedback came after counter-part playing
        need to implement this.
        '''
        pass

    # TODO: escalate to duel
    def feedback(self, next_state, reward, done):
        ''' feedback of each play - generally feedback came after counter-part playing
        call _feedback internally if train_mode is on
        '''
        self.history[-1].extend([next_state, reward, done])
        if self.is_train_mode:
            self._feedback(self.history[-1][self.HISTORY_STATE],     # state
                           self.history[-1][self.HISTORY_ACTION],     # action
                           # next_state
                           self.history[-1][self.HISTORY_NEXT_STATE],
                           self.history[-1][self.HISTORY_REWARD],     # reward
                           self.history[-1][self.HISTORY_DONE])     # done

    def _episode_feedback(self, reward):
        ''' feedback after full game finished.
        need to implement by process
        '''
        pass

    def episode_feedback(self, reward):
        ''' feedback after full game finished.
        call _episode_feedback internally if train_mode is on
        '''
        if self.is_train_mode:
            self._episode_feedback(reward)

    def save(self):
        ''' save player info to storage. please do not override it.
        please override serialize.
        '''
        serialized_obj = (self._elo, self._n_playes, self.serialize())
        with open(self.storage, 'wb') as f:
            # pickle.dump(serialized_obj, f)
            msgpack.pack(serialized_obj, f)
        pass

    def load(self):
        ''' load player info  from storage please do not override it.
        please override deserialize.
        '''
        try:
            with open(self.storage, 'rb') as f:
                data = f.read()
                # self._elo, self._n_playes, extra_obj = pickle.load(f)
                self._elo, self._n_playes, extra_obj = msgpack.unpack(f)
                self.deserialize(extra_obj)
        except Exception:
            self._elo = 1200
            self._n_playes = 0
            self.deserialize(None)

    def serialize(self):
        ''' implement serialize player specific info.
        Using super when need.
        '''
        return None

    def deserialize(self, data):
        ''' implement deserialize player specific info.
        if data = None, initialize it.
        Using super when need.
        '''
        pass

    @property
    def elo(self):
        return self._elo

    @elo.setter
    def elo(self, value):
        self._elo = int(value + 0.5)  # round up

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value


class RandomPlayer(AbstractPlayer):
    ''' random player '''
    def _choose(self, state, available_actions):
        return random.choice(available_actions)
