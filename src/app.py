from detector import detect
from note_head_detector import AllNoteHeadsDetector, WholeNoteHeadDetector, HalfNoteHeadDetector
from staff.symbol_extractor import SymbolExtractor
from staff.staff_remover import StaffRemover
from staff.staff_finder import StaffFinder
import sys
# import for classification
from knn.knn_classification import Classification
knn = Classification()

__author__ = 'Marek' + 'Matej'

import cv2
from matplotlib import pyplot as plt

# note name vector
name = ['E', 'F', 'G', 'A', 'H', 'C', 'D']

image = None

image = cv2.imread("../test_sheets/vltava.png", cv2.IMREAD_GRAYSCALE) # default image

# any command line arguments given? 
# if true, argv[1] is considered to be filename
if (len(sys.argv) > 1):
    image = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

# Check if file is image
if (image == None):
    print ""
    print "Specified file does is not an image!"
    print ""
    print "Rerun: " + sys.argv[0] + " [filename]"
    print "- [filename] is input image"
    exit()

# Otsu's thresholding after Gaussian filtering
blur_image = False
blurred_image = cv2.GaussianBlur(image, (3, 3), 0) if blur_image else image
_, binary_image = cv2.threshold(image, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

staff_finder = StaffFinder(binary_image)
head_detector = AllNoteHeadsDetector(staff_finder.space_line_height)
staff_remover = StaffRemover(staff_finder, binary_image)

# line height
h = staff_finder.space_line_height

# optimized font size
font_size = 3*h/40

image_without_staff_lines = staff_remover.remove_all() * 255

output_image = cv2.cvtColor(image_without_staff_lines, cv2.COLOR_GRAY2RGB)

# go through score line by line (row by row)
for staff in staff_finder.staffs_with_helper_lines:
    
    # cut out propper part of score
    line_l = image[staff[0] - h : staff[len(staff) - 1] + h , : ]
    # detect note heads
    heads = head_detector.heads(line_l, 0.65)

    # go through note heads
    for i, head in enumerate(heads):
        color = (0, 0, 255)
        # get head type
        if head_detector.detector_for_result[i] == WholeNoteHeadDetector:
            color = (0, 255, 0)
        if head_detector.detector_for_result[i] == HalfNoteHeadDetector:
            color = (0, 255, 255)
        
        # mark note head
        cv2.rectangle(output_image, (head.left, head.top + staff[0] - int(h)), (head.right, head.bottom + staff[0] - int(h)), color, 1)

        # compute note head center. need to invert Y axis
        center = staff[len(staff) - 1] + h - (staff[0] - h ) - (head.bottom + head.top)/2 - h # vpocet stredu, korekce
        pos = int(center/(h/2))
        # write note name
        cv2.putText(output_image, name[pos % 7], (head.right, head.top + staff[0] - int(h)), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 0, 255))

# extract symbols        
symbol_extractor = SymbolExtractor(image_without_staff_lines)

# plot all extracted symbols in bounding boxes
# also plot symbol types

for group in symbol_extractor.bounding_groups:
    color = (255, 0, 0,)
    cv2.rectangle(output_image, group[0].bottom_left, group[0].top_right, color, 1)
    
    box = group[0]
    symbol = image_without_staff_lines[box.bottom:box.top, box.left:box.right]
    # classify symbol
    what, dist = knn.classify(symbol)
    # if we know (or we think we know) what it is, PLOT IT!
    if (dist < 1e+08):
        cv2.putText(output_image, what ,box.bottom_left, cv2.FONT_HERSHEY_SIMPLEX, font_size, (0,255,0))


# plot lines back
for staff in staff_finder.staffs_with_helper_lines:
    for line_index in staff:
        cv2.line(output_image, (0, line_index), (output_image.shape[1], line_index), (220, 220, 220), 1)
for staff in staff_finder.staffs:
    for line_index in staff:
        cv2.line(output_image, (0, line_index), (output_image.shape[1], line_index), (110, 110, 110), 1)


# Show histogram
"""
plt.subplot(1, 2, 1)
plt.plot(xrange(staff_finder.histogram.shape[0]), staff_finder.histogram)
plt.title('Histogram')
plt.xticks([])
plt.yticks([])

plt.subplot(1, 2, 2)
#"""
# Show image with all the objects
#"""
plt.imshow(output_image)
plt.title('Result')
plt.xticks([])
plt.yticks([])

plt.show()
#"""