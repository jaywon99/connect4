''' PGN module '''

import numpy as np

# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

BETA = 0.00001

class DNN:
    ''' DNN class '''
    def __init__(self, layers, name="main", learning_rate=0.001):
        self.layers = layers
        self.net_name = name
        self.learning_rate = learning_rate
        self.session = None

        self._build_network()

    def _build_network(self):
        ''' build DNN network '''
        self.X = tf.placeholder(tf.float32, [None, self.layers[0]], name="input")
        self.Y = tf.placeholder(tf.float32, [None, self.layers[-1]], name="output")
        net = self.X
        for i in range(1, len(self.layers)-1):
            net = tf.layers.dense(net, self.layers[i], activation=tf.nn.relu)
        self.logits = tf.layers.dense(net, self.layers[-1])
        self.output = tf.nn.softmax(self.logits)
        self.chosen_action = tf.argmax(self.output, 1)

        self.reward_holder = tf.placeholder(shape=[None], dtype=tf.float32)
        self.action_holder = tf.placeholder(shape=[None], dtype=tf.int32)

        self.indexes = tf.range(0, tf.shape(self.output)[0]) * tf.shape(self.output)[1] + self.action_holder
        self.responsible_outputs = tf.gather(tf.reshape(self.output, [-1]), self.indexes)

        self.loss = - tf.reduce_mean(tf.log(self.responsible_outputs + 1e-9) * self.reward_holder)
        self.reg_losses = tf.identity(tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES, scope=self.name),
                                      name="reg_losses")

        reg_loss = BETA * tf.reduce_mean(self.reg_losses)
        total_loss = tf.add(self.loss, reg_loss, name="total_loss")

        self.train = tf.train.AdamOptimizer(self.learning_rate).minimize(total_loss)

    def set_session(self, session):
        ''' set tensorflow session '''
        self.session = session

    def predict(self, state):
        ''' get prediction result of state '''
        input_values = np.reshape(state, [-1, self.layers[0]])
        return self.session.run(self.output, feed_dict={self.X: input_values})

    def update(self, states, actions, rewards):
        ''' dnn update '''
        return self.session.run([self.loss, self.train],
                                {self.X: states,
                                 self.action_holder: actions,
                                 self.reward_holder: rewards})

    def save(self, filename):
        ''' save network variables '''
        saver = tf.train.Saver()
        saver.save(self.session, filename)

    def load(self, filename):
        ''' load network variables '''
        try:
            saver = tf.train.Saver()
            saver.restore(self.session, filename)
        except Exception as ex:
            print("Loading Exception", ex) # loading error - ignore
