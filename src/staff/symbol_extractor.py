import cv2
import numpy as np
from geometry import tuples2rectangles, group_rectangles, add_overlaying_rectangles

__author__ = 'Marek'


class SymbolExtractor:
    def __init__(self, image):
        self.image = np.array(image)
        self._bounding_groups = None
        self._contours = None
        self._contours_hierarchy = None

    def _do_it(self):
        # we can erode or dilate the image little bit
        #
        # kernel = np.ones((5, 5), np.uint8)
        # mask = np.ones(image_without_staff_lines.shape, np.uint8)
        # inverted_image = mask - image_without_staff_lines
        # dilate_image = cv2.dilate(inverted_image, kernel, iterations=1)

        self._contours, self._contours_hierarchy = cv2.findContours(self.image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        bounding_rectangles = tuples2rectangles(
            [cv2.boundingRect(contour) for contour, current_hierarchy in zip(self._contours, self._contours_hierarchy[0]) if
             current_hierarchy[3] >= 0])

        overlaying_rectangles = group_rectangles(bounding_rectangles)
        self._bounding_groups = add_overlaying_rectangles(overlaying_rectangles)

    @property
    def bounding_groups(self):
        if self._bounding_groups is None:
            self._do_it()

        return self._bounding_groups

    @property
    def contours(self):
        if self._contours is None:
            self._do_it()

        return self._contours

    @property
    def contours_hierarchy(self):
        if self._contours_hierarchy is None:
            self._do_it()

        return self._contours_hierarchy
