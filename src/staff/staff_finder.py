__author__ = 'Marek'

import numpy as np


class StaffFinder:
    STAFF_LINES = 5
    THRESHOLD = 0.8

    def __init__(self, image):
        self.image = image
        self._histogram = None
        self._line_height = None
        self._line_width = None
        self._space_height = None
        self._line_indices = None

    @property
    def histogram(self):
        """
        Lazy evaluation of y axis histogram.
        :return: array of values
        """
        if self._histogram is None:
            self._histogram = (np.ones(self.image.shape) - self.image).sum(dtype=np.int32, axis=1)
            maximum = np.amax(self._histogram)
            self._histogram[self._histogram[:] < maximum * self.THRESHOLD] = 0
        return self._histogram

    @property
    def line_indices(self):
        """
        Returns array of indices corresponding to start index of line.

        :return:
        """
        if self._line_indices:
            return self._line_indices

        indices = []
        previous_value = 0
        index = 0
        for value in self.histogram:
            if value > 0 and previous_value <= 0:
                indices.append(index)

            previous_value = value
            index += 1
        self._line_indices = indices

        return self._line_indices

    @property
    def line_height(self):
        """
        Basically it returns average of uninterrupted runs through histogram
        :return:
        """
        if self._line_height:
            return self._line_height

        heights = []

        for start_index in self.line_indices:
            end_index = start_index+1
            while self.histogram[end_index] > 0:
                end_index += 1
            heights.append(end_index - start_index + 1)

        self._line_height = max(heights)
        return self._line_height

    @property
    def space_height(self):
        if self._space_height:
            return self._space_height

        heights = []

        line_order = 0
        prev_line_index = -1
        for line_index in self.line_indices:
            line_order += 1

            if prev_line_index > 0:
                heights.append(line_index-prev_line_index-self.line_height)

            prev_line_index = line_index

            if line_order >= self.STAFF_LINES:
                line_order = 0
                prev_line_index = -1

        self._space_height = np.average(heights)
        return self._space_height