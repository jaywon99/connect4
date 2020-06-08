''' DNN module '''

import numpy as np

import keras
from keras.models import Sequential, load_model, clone_model
from keras.layers import Dense, Activation
from keras.optimizers import Adam


class DNN:
    ''' DNN class '''

    def __init__(self, layers, name="main", learning_rate=0.001):
        self.layers = layers
        self.net_name = name
        self.learning_rate = learning_rate

        self._build_network()

    def _build_network(self):
        ''' build DNN network '''
        self.model = Sequential()
        self.model.add(Dense(self.layers[1], input_shape=(self.layers[0],)))
        self.model.add(Activation('relu'))
        for i in range(2, len(self.layers) - 1):
            self.model.add(Dense(self.layers[i]))
            self.model.add(Activation('relu'))
        self.model.add(Dense(self.layers[-1]))

        # # self.loss = tf.losses.softmax_cross_entropy(self.Y, self.Q)
        # # self.train = tf.train.RMSPropOptimizer(self.learning_rate, decay=0.75).minimize(self.loss)
        self.model.compile(loss=keras.losses.mean_squared_error, optimizer=Adam(
            learning_rate=self.learning_rate), metrics=['accuracy'])

    def predict(self, state):
        ''' get prediction result of state '''
        input_values = np.reshape(state, [-1, self.layers[0]])
        return self.model.predict(input_values)

    def update(self, x_stack, y_stack):
        ''' dnn update '''
        # fit(x=None, y=None, batch_size=None, epochs=1, verbose=1, callbacks=None, validation_split=0.0, validation_data=None, shuffle=True, class_weight=None, sample_weight=None, initial_epoch=0, steps_per_epoch=None, validation_steps=None, validation_freq=1, max_queue_size=10, workers=1, use_multiprocessing=False)
        hist = self.model.fit(x=x_stack, y=y_stack, epochs=10, verbose=0)
        return hist.history['loss'], None

    def _filename_with_extension(self, filename):
        return filename + ".h5"

    def save(self, filename):
        ''' save network variables '''
        self.model.save(self._filename_with_extension(filename))

    def load(self, filename):
        ''' load network variables '''
        try:
            self.model = load_model(self._filename_with_extension(filename))
        except Exception:
            print("Loading Exception")  # loading error - ignore

    def clone(self, name):
        c = DNN(self.layers, name, self.learning_rate)
        c.model = clone_model(self.model)
        c.model.set_weights(self.model.get_weights())
        return c

    def set_weights(self, weights):
        self.model.set_weights(weights)

    def get_weights(self):
        return self.model.get_weights()
