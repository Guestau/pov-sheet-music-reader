import numpy as np
import cv2
from matplotlib import pyplot as plt
from knn_classification import Classification
import os.path

knn = Classification()

# yvector = ['#', 'b', '1', '2', '4', '8', '8s', '16', '16s', 'k', 'o', 'p', 'p4', 'p8', 'p16', 't', 'pnt', 'tnc', 't2',
#           't3', 't4', 't34', 't68', 'tc']
ycount = len(knn.yvector)

# test klasifikatoru
def testClassification():
    #print '   ', knn.yvector
    testarray = []
    for pattern in knn.yvector:
        index = 3 * knn.xcount / 4
        testvec = []
        for i in knn.yvector:
            #testvec[knn.yvector.index(i)] = 0
            testvec.append(0)
        path = '../../training/' + pattern + '/' + pattern + '(' + str(index) + ').png'
        while os.path.exists(path):
            img = cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            what, dist = knn.classify(img)
            #print pattern, what, knn.yvector.index(what)
            testvec[knn.yvector.index(what)] += 1
            index += 1
            path = '../../training/' + pattern + '/' + pattern + '(' + str(index) + ').png'
        testarray.append(testvec)
        #print pattern, testvec
    return testarray

size = ycount * knn.ybox, knn.xcount * knn.xbox
dataset = np.zeros(size, dtype=np.uint8)

y = 0
for j in knn.yvector:
    for i in range(knn.xcount):
        img = cv2.imread('../../training/' + j + '/' + j + '(' + str(i) + ').png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
        # print j+'('+str(i)+').png'
        im_bw = cv2.bitwise_not(cv2.resize(img,(100,100)))
        x = i * knn.xbox
        dataset[y:y + im_bw.shape[0], x:x + im_bw.shape[1]] = im_bw
    y = y + knn.ybox

cv2.imwrite('dataset.png', dataset)

# split the image to 'size' cells, each 'xbox'x'ybox' size
cells = [np.hsplit(row, knn.xcount) for row in np.vsplit(dataset, ycount)]

# Make it into a Numpy array. It size will be ('xcout','ycount','xbox','ybox') #(50,100,20,20)
x = np.array(cells)

# Now we prepare train_data and test_data.
train = x[:, :3 * knn.xcount / 4].reshape(-1, knn.xbox * knn.ybox).astype(np.float32)  # Size = (xcout*ycount/2,xbox*ybox)
test = x[:, 3 * knn.xcount / 4:knn.xcount].reshape(-1, knn.xbox * knn.ybox).astype(np.float32)  # Size = (xcout*ycount/2,xbox*ybox)

# Create labels for train and test data
k = np.arange(ycount)
train_labels = np.repeat(k, 3 * knn.xcount / 4)[:, np.newaxis]
test_labels = np.repeat(k, knn.xcount / 4)[:, np.newaxis]

# Initiate kNN, train the data, then test it
knn.knn.train(train, train_labels)
ret, result, neighbours, dist = knn.knn.find_nearest(test, k=5)

# Now we check the accuracy of classification
# For that, compare the result with test_labels and check which are wrong
matches = result == test_labels
correct = np.count_nonzero(matches)
accuracy = correct * 100.0 / result.size
print accuracy
'''
# save the data
np.savez('knn_data.npz', train=train, train_labels=train_labels)

# Now load the data
with np.load('knn/knn_data.npz') as data:
    print data.files
    train = data['train']
    train_labels = data['train_labels']
'''
'''
# test
for i in range(17):
    img = cv2.imread('../../training/abc/abc(' + str(50 + i) + ').png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    # print ret,result,neighbours,dist
    # print ret,yvector[int(ret)], dist[0][0]
    what, dist = knn.classify(img)
    print what, dist
'''

#vypis testu klasifikatoru
tstarr = testClassification()
print "   ", knn.yvector
for i in knn.yvector:
    print i, tstarr[knn.yvector.index(i)]