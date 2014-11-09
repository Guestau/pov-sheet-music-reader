import utils
from staff.staff_remover import StaffRemover
from staff.staff_finder import StaffFinder

__author__ = 'Marek'

import cv2
import numpy as np
from matplotlib import pyplot as plt


image = cv2.imread("../test_sheets/mafia_main_theme/mafia_main_theme-1.png", cv2.IMREAD_GRAYSCALE)

# Otsu's thresholding after Gaussian filtering
blur_image = True
blurred_image = cv2.GaussianBlur(image, (3, 3), 0) if blur_image else image
return_value, binary_image = cv2.threshold(image, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

staff_finder = StaffFinder(binary_image)
staff_remover = StaffRemover(staff_finder, binary_image)
image_without_staff_lines = staff_remover.remove_all() * 255

output_image = cv2.cvtColor(image_without_staff_lines, cv2.COLOR_GRAY2RGB)

# kernel = np.ones((5, 5), np.uint8)
# mask = np.ones(image_without_staff_lines.shape, np.uint8)
# inverted_image = mask - image_without_staff_lines
# dilate_image = cv2.dilate(inverted_image, kernel, iterations=1)

contours, hierarchy = cv2.findContours(image_without_staff_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# output_image = cv2.GaussianBlur(output_image, (9, 9), 0)
# cv2.drawContours(output_image, contours, -1, (0, 255, 0), 3)

bounding_rectangles = [cv2.boundingRect(contour) for contour, current_hierarchy in zip(contours, hierarchy[0]) if
                       current_hierarchy[3] == 0]

overlap_rectangles = []
for rectangle in bounding_rectangles:
    interact = False
    for group in overlap_rectangles:
        if any(group_item for group_item in group if utils.any_rect_interaction(rectangle, group_item)):
            interact = True
            group.append(rectangle)
            break
    if not interact:
        overlap_rectangles.append([rectangle])

merged_bounding_rectangles = []
for group in overlap_rectangles:
    if len(group) > 1:
        min_x = min(group, key=lambda t: t[0])
        min_y = min(group, key=lambda t: t[1])
        max_x = max(group, key=lambda t: t[0] + t[2])
        max_y = max(group, key=lambda t: t[1] + t[3])

        merged_group = (min_x[0], min_y[1], max_x[0] + max_x[2] - min_x[0], max_y[1] + max_y[3] - min_y[1],)
        merged_bounding_rectangles.append(merged_group)
    else:
        merged_bounding_rectangles.append(group[0])

for rectangle in merged_bounding_rectangles:
    color = (255, 0, 0,)
    x, y, w, h = rectangle
    cv2.rectangle(output_image, (x, y), (x + w, y + h), color, 2)


# ## PLOT ALL SHITS

# plt.subplot(1, 2, 1)
# plt.plot(xrange(staff_finder.histogram.shape[0]), staff_finder.histogram)
# plt.title('Histogram')
# plt.xticks([])
# plt.yticks([])

# plt.subplot(1, 2, 2)
plt.imshow(output_image, 'gray')
plt.title('Otsu\'s Thresholding')
plt.xticks([])
plt.yticks([])

plt.show()
