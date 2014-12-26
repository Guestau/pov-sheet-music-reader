import cv2
import itertools
import numpy as np
from matplotlib import pyplot as plt
from geometry import Rectangle, group_rectangles, add_overlaying_rectangles
from staff.staff_finder import StaffFinder
from staff.staff_remover import StaffRemover

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
        w, h = self.template.shape

        return [Rectangle(pt[0], pt[1], h, w) for pt in zip(*points[::-1])]


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


class AllNoteHeadsDetector(NoteHeadDetector):
    def __init__(self, staff_line_space):
        self.detectors = [BlackNoteHeadDetector(staff_line_space), WholeNoteHeadDetector(staff_line_space),
                          HalfNoteHeadDetector(staff_line_space)]
        self.results = dict()

    def heads(self, segment, threshold=0.65):
        for detector in self.detectors:
            self.results[detector.__class__] = detector.heads(segment, threshold)

        return list(itertools.chain(*self.results.values()))

    def detected_by(self, rectangle):
        """

        :param rectangle:
        :return: vrati tridu detektoru, ktery nasel rectangle
        """
        for detector in self.detectors:
            if rectangle in self.results[detector.__class__]:
                return detector.__class__
        return None


if __name__ == '__main__':
    img = cv2.imread("../test_sheets/mam_jizvu_na_rtu_noty/mam_jizvu_na_rtu_noty-1.png", cv2.IMREAD_GRAYSCALE)
    # img = cv2.imread("../test_sheets/test1.png", cv2.IMREAD_GRAYSCALE)

    org = img.copy()

    return_value, binary_image = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    staff_finder = StaffFinder(binary_image)
    # staff_remover = StaffRemover(staff_finder, binary_image)
    # image_without_staff_lines = staff_remover.remove_all()
    # img = image_without_staff_lines * 255
    line_height = staff_finder.line_height + staff_finder.space_height

    detector = AllNoteHeadsDetector(line_height)
    rectangles = detector.heads(org, 0.65)

    output_image = cv2.cvtColor(org, cv2.COLOR_GRAY2RGB)
    for rec in rectangles:
        cv2.rectangle(output_image, rec.top_left, rec.bottom_right, (0, 0, 255), 1)

    plt.imshow(output_image)

    plt.show()

