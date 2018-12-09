import random

import numpy as np


class BatchManager:

    def __init__(self, settings):
        self._nbStates = settings['ndStates']

        self._maxMemory = settings['maxMemory']
        self._batchSize = settings['batchSize']

        self.current_state = np.empty((self._maxMemory, self._nbStates), dtype=np.float32)
        self.next_state = np.empty((self._maxMemory, self._nbStates), dtype=np.float32)

        self.actions = np.zeros(self._maxMemory, dtype=np.uint8)
        self.rewards = np.empty(self._maxMemory, dtype=np.int8)

        self.length = 0
        self.index = 0

    def add_data(self, current_state, next_state, action, reward):
        self.current_state[self.index, ...] = current_state
        self.next_state[self.index, ...] = next_state

        self.actions[self.index] = action
        self.rewards[self.index] = reward

        self.length = max(self.length, self.index + 1)
        self.index = (self.index + 1) % self._maxMemory

    def get_batch(self, sess, target_function):
        memory_length = self.length
        chosen_batch_size = min(self._batchSize, memory_length)

        currents = np.zeros((chosen_batch_size, self._nbStates))
        targets = np.zeros((chosen_batch_size, self._nbStates))

        for index in range(chosen_batch_size):

            random_index = random.randrange(0, memory_length)

            current_state = self.current_state[random_index]
            next_state = self.next_state[random_index]
            action = self.actions[random_index]
            reward = self.rewards[random_index]

            currents[index], targets[index] = target_function(sess, current_state, next_state, action, reward)

        return currents, targets
