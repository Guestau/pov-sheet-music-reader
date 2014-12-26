import hashlib
import os
from staff.symbol_extractor import SymbolExtractor
from staff.staff_remover import StaffRemover
from staff.staff_finder import StaffFinder
# import for classification
from knn_classification import Classification

from note_head_detector import NoteHeadDetector

__author__ = 'Marek'

import cv2
from matplotlib import pyplot as plt


# image = cv2.imread("../test_sheets/vltava.png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_sheets/Den_preslavny_Tenor.png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_sheets/Requiem_for_a_Dream/Requiem_for_a_Dream-1.png", cv2.IMREAD_GRAYSCALE)
image = cv2.imread("../test_noty/test16/test16(3).png", cv2.IMREAD_GRAYSCALE)
# image = cv2.imread("../test_noty/test_artikulace_repetice/test_rep_both.png", cv2.IMREAD_GRAYSCALE)

# Otsu's thresholding after Gaussian filtering
blur_image = False
blurred_image = cv2.GaussianBlur(image, (3, 3), 0) if blur_image else image
_, binary_image = cv2.threshold(image, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

staff_finder = StaffFinder(binary_image)
staff_remover = StaffRemover(staff_finder, binary_image)

image_without_staff_lines = staff_remover.remove_all() * 255
symbol_extractor = SymbolExtractor(image_without_staff_lines)

# ## PLOT ALL SHITS
output_image = cv2.cvtColor(image_without_staff_lines, cv2.COLOR_GRAY2RGB)

for group in symbol_extractor.bounding_groups:
    color = (255, 0, 0,)
    cv2.rectangle(output_image, group[0].bottom_left, group[0].top_right, color, 1)

for line_index in staff_finder.line_indices:
    cv2.line(output_image, (0, line_index), (output_image.shape[1], line_index), (200, 200, 200), 1)
'''
i = 0
for group in symbol_extractor.bounding_groups:
    box = group[0]
    symbol = image_without_staff_lines[box.bottom:box.top, box.left:box.right]
    file_name = "9(" + str(i) + ")"+str(symbol.shape[1])#hashlib.sha1(symbol).hexdigest()
    i += 1
    cv2.imwrite("..\\tmp\\" + file_name + ".png", symbol, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
#    cv2.imwrite(os.path.dirname(os.path.abspath(__file__)) + "\\..\\tmp\\" + file_name + ".png", symbol, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
'''
# plt.subplot(1, 2, 1)
# plt.plot(xrange(staff_finder.histogram.shape[0]), staff_finder.histogram)
# plt.title('Histogram')
# plt.xticks([])
# plt.yticks([])

width_note = 45
note_detect = NoteHeadDetector(staff_finder.space_height,cv2.imread("../resources/black_head2.png", cv2.IMREAD_GRAYSCALE))
# train KNearestNeighbour
knn = Classification()
# trying classification
i=0
for group in symbol_extractor.bounding_groups:
    i+=1
    box = group[0]
    symbol = image_without_staff_lines[box.bottom:box.top, box.left:box.right]
    if symbol.shape[0] > knn.ybox or symbol.shape[1] > knn.xbox:
        refx = -11
        count = 0
        listrefx = []
        for rect in note_detect.heads(symbol):
            listrefx.append(rect.x)
        listrefx.sort()
        for x in listrefx:
            if abs(refx - x) > 10:
                count += 1
                refx = x
        width = symbol.shape[1] / count
        # print width , count , symbol.shape[1], note_detect.heads(symbol)
        startx = 0
        for k in range(width,symbol.shape[1],width):
            sym = symbol[:, startx:k]
            what, distance= knn.classify(sym)
            print 'co,x,y,vzdalenost(0=ok):', what, box.bottom, box.left + startx, distance
            file_name = what + '_' + str(i) + '_' + str(k)
            if distance == 0.0:
                file_name = 'ok_'+ file_name
            cv2.imwrite("..\\tmp\\" + file_name + ".png", sym, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            startx = k
        continue
    what, distance= knn.classify(symbol)
    print 'co,x,y,vzdalenost(0=ok):', what, box.bottom, box.left, distance
    file_name = what + '_' + str(i)
    if distance == 0.0:
        file_name = 'ok_'+ file_name
    cv2.imwrite("..\\tmp\\" + file_name + ".png", symbol, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

# plt.subplot(1, 2, 2)
plt.imshow(output_image)
plt.title('Result')
plt.xticks([])
plt.yticks([])

plt.show()