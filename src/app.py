from detector import detect
from note_head_detector import AllNoteHeadsDetector, WholeNoteHeadDetector, HalfNoteHeadDetector
from staff.symbol_extractor import SymbolExtractor
from staff.staff_remover import StaffRemover
from staff.staff_finder import StaffFinder
import sys
# import for classification

__author__ = 'Marek'

import cv2
from matplotlib import pyplot as plt

image = None

image = cv2.imread("../test_sheets/vltava.png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_sheets/mafia_main_theme/mafia_main_theme-1.png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_sheets/test1.png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_sheets/Den_preslavny_Tenor.png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_sheets/Requiem_for_a_Dream/Requiem_for_a_Dream-1.png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_noty/test16/test16(3).png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_noty/test1/test1(1).png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_noty/test_artikulace_repetice/test_rep_both.png", cv2.IMREAD_GRAYSCALE)

# any command line arguments given? 
# if true, argv[1] is considered to be filename
if (len(sys.argv) > 1):
    image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

# Check if file is image
if (image == None):
    print ""
    print "Specified file does is not an image!"
    print ""
    print "Rerun " + sys.argv[0] + " [filename]"
    print "- [filename] is input image"
    exit()

# Otsu's thresholding after Gaussian filtering
blur_image = False
blurred_image = cv2.GaussianBlur(image, (3, 3), 0) if blur_image else image
_, binary_image = cv2.threshold(image, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

staff_finder = StaffFinder(binary_image)
head_detector = AllNoteHeadsDetector(staff_finder.space_line_height)
notes_heads = head_detector.heads(image, 0.65)
staff_remover = StaffRemover(staff_finder, binary_image)

image_without_staff_lines = staff_remover.remove_all() * 255
symbol_extractor = SymbolExtractor(image_without_staff_lines)

# i = 0
# for group in symbol_extractor.bounding_groups:
#     box = group[0]
#     symbol = image_without_staff_lines[box.bottom:box.top, box.left:box.right]
#     file_name = "9(" + str(i) + ")"+str(symbol.shape[1])#hashlib.sha1(symbol).hexdigest()
#     i += 1
#     cv2.imwrite("..\\tmp\\" + file_name + ".png", symbol, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
#     cv2.imwrite(os.path.dirname(os.path.abspath(__file__)) + "\\..\\tmp\\" + file_name + ".png", symbol, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

# detect(staff_finder, symbol_extractor, image_without_staff_lines)

# ## PLOT ALL SHITS
output_image = cv2.cvtColor(image_without_staff_lines, cv2.COLOR_GRAY2RGB)

for group in symbol_extractor.bounding_groups:
    color = (255, 0, 0,)
    cv2.rectangle(output_image, group[0].bottom_left, group[0].top_right, color, 1)

for staff in staff_finder.staffs_with_helper_lines:
    for line_index in staff:
        cv2.line(output_image, (0, line_index), (output_image.shape[1], line_index), (220, 220, 220), 1)

for i, head in enumerate(notes_heads):
    color = (0, 0, 255)
    if head_detector.detector_for_result[i] == WholeNoteHeadDetector:
        color = (0, 255, 0)
    if head_detector.detector_for_result[i] == HalfNoteHeadDetector:
        color = (0, 255, 255)

    cv2.rectangle(output_image, head.top_left, head.bottom_right, color, 1)

# plt.subplot(1, 2, 1)
# plt.plot(xrange(staff_finder.histogram.shape[0]), staff_finder.histogram)
# plt.title('Histogram')
# plt.xticks([])
# plt.yticks([])

# plt.subplot(1, 2, 2)
#"""
plt.imshow(output_image)
plt.title('Result')
plt.xticks([])
plt.yticks([])

plt.show()
#"""