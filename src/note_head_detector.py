import cv2
import numpy as np
from matplotlib import pyplot as plt
from src.geometry import Rectangle, group_rectangles, add_overlaying_rectangles
from src.staff.staff_finder import StaffFinder
from src.staff.staff_remover import StaffRemover

__author__ = 'Marek'


class NoteHeadDetector:

    def __init__(self, staff_line_space, template):
        self.staff_line_space = staff_line_space
        self.template = cv2.resize(template, (0, 0), fx=staff_line_space / template.shape[0], fy=staff_line_space / template.shape[0])

    def heads(self, segment, threshold=0.7):
        if segment.shape[0] < self.staff_line_space or segment.shape[1] < self.staff_line_space:
            return

        result = cv2.matchTemplate(img, self.template, cv2.TM_CCOEFF_NORMED)
        points = np.where(result >= threshold)
        w, h = self.template.shape

        return [Rectangle(pt[0], pt[1], w, h) for pt in zip(*points[::-1])]

if __name__ == '__main__':
    # img = cv2.imread("../tmp/3cc3267600c603a13870a22d17fbed1d5da6f01c.png", cv2.IMREAD_GRAYSCALE)
    # img = cv2.imread("../test_sheets/mam_jizvu_na_rtu_noty/mam_jizvu_na_rtu_noty-1.png", cv2.IMREAD_GRAYSCALE)
    # line_height = 12.0
    img = cv2.imread("../test_sheets/vltava.png", cv2.IMREAD_GRAYSCALE)
    # line_height = 9.0

    return_value, binary_image = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    staff_finder = StaffFinder(binary_image)
    staff_remover = StaffRemover(staff_finder, binary_image)
    image_without_staff_lines = staff_remover.remove_all()

    img = image_without_staff_lines*255
    line_height = staff_finder.line_height + staff_finder.space_height

    org = img.copy()
    template = cv2.imread("../resources/black_head.png", cv2.IMREAD_GRAYSCALE)

    detector = NoteHeadDetector(line_height, cv2.imread("../resources/black_head.png", cv2.IMREAD_GRAYSCALE))
    rectangles = detector.heads(img, 0.7)

    output_image = cv2.cvtColor(org, cv2.COLOR_GRAY2RGB)
    for rec in rectangles:
        cv2.rectangle(output_image, rec.top_left, rec.bottom_right, (0, 0, 255), 1)

    plt.imshow(output_image)
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(142)
    # plt.imshow(img, cmap='gray')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    #
    # plt.subplot(143)
    # plt.imshow(org, cmap='gray')
    #
    # plt.subplot(144)
    # plt.imshow(template, cmap='gray')

    plt.show()

