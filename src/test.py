'''
Run python test.py [N] [output]
    [N] test size (default = 100)
    [output] output file (default = ../matrix.txt)
    
Expects test&training data in ../training/
'''
__author__ = 'Matej'

import numpy as np
import cv2
from matplotlib import pyplot as plt
from knn.knn_classification import Classification
import os.path
import random
import sys

knn = Classification()

ycount = len(knn.yvector)
# create training set
full_set_size = 1001
full_set = []
for i in range(full_set_size): full_set.append(i)

# create testing set - get count
if (len(sys.argv) > 1):
    if (int(sys.argv[1]) < full_set_size):
        test_set_size = int(sys.argv[1])
    else:
        test_set_size = full_set_size
else:
    test_set_size = full_set_size/10

subset_rest = random.sample(full_set, test_set_size)

if (len(sys.argv) > 2):
    filename = sys.argv[2]
else:
    filename = "../matrix.txt"
    
print "Set size:",len(subset_rest)
print ""
good = 0
bad = 0
matrix = dict()

for x in knn.yvector:
    vec = dict()
    for y in knn.yvector:
        vec[y] = 0
    matrix[x] = vec

for j in knn.yvector:
    print "Testing:", j, "..."
    for i in subset_rest:
        img = cv2.imread('../training/' + j + '/' + j + '(' + str(i) + ').png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
        if (img != None):
            what, dist = knn.classify(img)
            if (j == what): good += 1
            else: bad += 1
            matrix[j][what] += 1
            # print "Expected:", j, "Got:", what, "Dist:", dist
print ""
print "Good:", good
print "Bad:", bad

print "Accuracy:", good*100.0/(test_set_size*len(knn.yvector)), "%"

# write matrix to file
file = open(filename, "w")
for i in knn.yvector: 
    file.write("\t" + i)
file.write("\r\n")

for i in knn.yvector: 
    file.write(i)
    for j in knn.yvector:
        file.write("\t" + str(matrix[i][j]))
    file.write("\r\n")

file.close()




