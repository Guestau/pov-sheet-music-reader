import itertools

import cv2
import numpy as np

from geometry import Rectangle


__author__ = 'Marek'


class NoteHeadDetector:
    def __init__(self, staff_line_space, template):
        self.staff_line_space = staff_line_space
        self.template = cv2.resize(template, (0, 0), fx=staff_line_space / template.shape[0],
                                   fy=staff_line_space / template.shape[0])

    def heads(self, segment, threshold=0.65):
        if segment.shape[0] < self.staff_line_space or segment.shape[1] < self.staff_line_space:
            return

        # result = cv2.matchTemplate(img, self.template, cv2.TM_CCOEFF_NORMED)
        result = cv2.matchTemplate(segment, self.template, cv2.TM_CCOEFF_NORMED)
        points = np.where(result >= threshold)
        h, w = self.template.shape

        return [Rectangle(pt[0], pt[1], w, h) for pt in zip(*points[::-1])]


class BlackNoteHeadDetector(NoteHeadDetector):
    def __init__(self, staff_line_space):
        NoteHeadDetector.__init__(self, staff_line_space,
                                  cv2.imread("../resources/black_note.png", cv2.IMREAD_GRAYSCALE))


class WholeNoteHeadDetector(NoteHeadDetector):
    def __init__(self, staff_line_space):
        NoteHeadDetector.__init__(self, staff_line_space,
                                  cv2.imread("../resources/whole_note.png", cv2.IMREAD_GRAYSCALE))


class HalfNoteHeadDetector(NoteHeadDetector):
    def __init__(self, staff_line_space):
        NoteHeadDetector.__init__(self, staff_line_space,
                                  cv2.imread("../resources/half_note.png", cv2.IMREAD_GRAYSCALE))


class AllNoteHeadsDetector:
    def __init__(self, staff_line_space, detectors=None):
        self.detectors = [BlackNoteHeadDetector(staff_line_space), WholeNoteHeadDetector(staff_line_space),
                          HalfNoteHeadDetector(staff_line_space)] if detectors is None else detectors
        self._clear()

    def _clear(self):
        # hashmap detector.__class__ : [Rectangles]
        self.result_by_class = dict()
        # [Rectangles]
        self.list_result = []
        # [detector.__class__] corresponding to list_result
        self.detector_for_result = []

    def heads(self, segment, threshold=0.65):
        self._clear()

        for detector in self.detectors:
            result = detector.heads(segment, threshold)
            self.result_by_class[detector.__class__] = result
            self.detector_for_result += [detector.__class__]*len(result)

        self.list_result = list(itertools.chain(*self.result_by_class.values()))
        return self.list_result

    def detected_by(self, rectangle):
        """

        :param rectangle:
        :return: vrati tridu detektoru, ktery nasel rectangle
        """
        return self.detector_for_result[self.list_result.index(rectangle)]