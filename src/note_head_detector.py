import cv2
from matplotlib import pyplot as plt
from src.staff.staff_finder import StaffFinder
from src.staff.staff_remover import StaffRemover

__author__ = 'Marek'


class NoteHeadDetector:

    def __init__(self, staff_line_space):
        self.staff_line_space = staff_line_space
        template = cv2.imread("../resources/black_head.png", cv2.IMREAD_GRAYSCALE)
        self.template = cv2.resize(template, (0, 0), fx=line_height / template.shape[0], fy=line_height / template.shape[0])

    def head_position(self, segment, threshold=0.5, take_min=True):
        if segment.shape[0] < self.staff_line_space or segment.shape[1] < self.staff_line_space:
            return

        res = cv2.matchTemplate(segment, self.template, cv2.TM_SQDIFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if (take_min and min_val > threshold) or (not take_min and max_val < threshold):
            return

        position = min_loc if take_min else max_loc
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        w, h = self.template.shape
        # position[0] += w/2
        # position[1] += h/2

        return position

if __name__ == '__main__':
    # img = cv2.imread("../tmp/3cc3267600c603a13870a22d17fbed1d5da6f01c.png", cv2.IMREAD_GRAYSCALE)
    img = cv2.imread("../test_sheets/vltava.png", cv2.IMREAD_GRAYSCALE)
    return_value, binary_image = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    staff_finder = StaffFinder(binary_image)
    staff_remover = StaffRemover(staff_finder, binary_image)
    image_without_staff_lines = staff_remover.remove_all()

    img = image_without_staff_lines*255

    org = img.copy()
    line_height = 9.0
    template = cv2.imread("../resources/black_head.png", cv2.IMREAD_GRAYSCALE)
    template = cv2.resize(template, (0, 0), fx=line_height / template.shape[0], fy=line_height / template.shape[0])
    w, h = template.shape

    res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img, top_left, bottom_right, 128, 1)

    # plt.subplot(141)
    # res[res > 0.5] = 1
    plt.imshow(res, cmap='gray')
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

