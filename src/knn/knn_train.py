import numpy as np
import cv2
from knn_classification import Classification
import os.path
import random

knn = Classification()

ycount = len(knn.yvector)
# create training set
full_set_size = 1001
full_set = []
for i in range(full_set_size): full_set.append(i)
subset = random.sample(full_set, knn.xcount)


# Test classifier
def testClassification():
    #print '   ', knn.yvector
    testarray = []
    for pattern in knn.yvector:
        index = 3 * knn.xcount / 4
        testvec = []
        for i in knn.yvectorb:
            testvec.append(0)
        path = '../../training/' + pattern + '/' + pattern + '(' + str(index) + ').png'
        while os.path.exists(path):
            img = cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            what, dist = knn.classify(img)
            testvec[knn.yvector.index(what)] += 1
            index += 1
            path = '../../training/' + pattern + '/' + pattern + '(' + str(index) + ').png'
        testarray.append(testvec)
        #print pattern, testvec
    return testarray

# Training classifier
size = ycount * knn.ybox, knn.xcount * knn.xbox
dataset = np.zeros(size, dtype=np.uint8)

y = 0
for j in knn.yvector:
    x = 0
    for i in subset:
        img = cv2.imread('../../training/' + j + '/' + j + '(' + str(i) + ').png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
        #print j+'('+str(i)+').png'
        im_bw = cv2.bitwise_not(cv2.resize(img,(100,100)))
        dataset[y:y + im_bw.shape[0], x:x + im_bw.shape[1]] = im_bw
        x += knn.xbox
    y = y + knn.ybox

cv2.imwrite('dataset.png', dataset)

print "Subset of samples (index numbers):"
print subset

# Split the image to 'size' cells, each 'xbox'x'ybox' size
cells = [np.hsplit(row, knn.xcount) for row in np.vsplit(dataset, ycount)]

# Make it into a Numpy array. It size will be ('xcout','ycount','xbox','ybox')
x = np.array(cells)

# Now we prepare train_data 
train = x[:, : knn.xcount ].reshape(-1, knn.xbox * knn.ybox).astype(np.float32)

# Create labels for training data
k = np.arange(ycount)
train_labels = np.repeat(k,  knn.xcount )[:, np.newaxis]

# Initiate kNN, train the data
knn.knn.train(train, train_labels)

# Save the data
np.savez('knn_data.npz', train=train, train_labels=train_labels)
print "Trained data saved"

