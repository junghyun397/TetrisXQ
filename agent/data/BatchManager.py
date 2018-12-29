import random

import numpy as np


class BatchManager:

    def __init__(self, settings):
        self._action = settings.ACTIONS
        self._states = settings.STATES

        self._max_memory = settings.MAX_MEMORY
        self._batch_size = settings.BATCH_SIZE

        self._current_state = np.empty((self._max_memory, self._states), dtype=np.float32)
        self._next_state = np.empty((self._max_memory, self._states), dtype=np.float32)

        self._actions = np.zeros(self._max_memory, dtype=np.uint8)
        self._rewards = np.empty(self._max_memory, dtype=np.int8)

        self._length = 0
        self._index = 0

    def add_data(self, current_state, next_state, action, reward):
        self._current_state[self._index, ...] = current_state
        self._next_state[self._index, ...] = next_state

        self._actions[self._index] = action
        self._rewards[self._index] = reward

        self._index = self._index % self._max_memory
        self._length = min(self._length + 1, self._max_memory)

    def get_batch(self, sess, target_function):
        chosen_batch_size = min(self._batch_size, self._length)

        currents = np.zeros((chosen_batch_size, self._states))
        targets = np.zeros((chosen_batch_size, self._action))

        for index in range(chosen_batch_size):

            random_index = random.randrange(0, self._length)

            current_state = self._current_state[random_index].reshape(1, self._states)
            next_state = self._next_state[random_index].reshape(1, self._states)
            action = self._actions[random_index]
            reward = self._rewards[random_index]

            currents[index], targets[index] = target_function(sess, current_state, next_state, action, reward)

        return currents, targets
