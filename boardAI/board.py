

class AbstractBoard:
    def __init__(self):
        self._end = False

    @classmethod
    def class_name(cls):
        return cls.__name__

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    def reset(self):
        self.end = False

    def get_colors(self):
        ''' get board colors (ex: tic-tac-toe = ['O', 'X'], chess = ['black', 'white], etc)
        '''
        raise NotImplementedError

    def render(self, mode='human'):
        ''' display board '''
        raise NotImplementedError

    def get_status(self, color):
        ''' return status by color and available actions. should be implemented at derived classed '''
        raise NotImplementedError

    def play(self, action, color):
        ''' play action and get result. (not return next state)
        reward (if possible, depend on game), result (Check Const)
        '''
        raise NotImplementedError
