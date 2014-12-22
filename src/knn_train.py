import numpy as np
import cv2
from matplotlib import pyplot as plt
# box with note
xbox = 65
ybox = 150
# number pattern and count
xcount = 200
yvector = ['#','b','2','4','8','16','k','o','p4','p8','p16']
ycount = len(yvector)

size = ycount * ybox, xcount * xbox
dataset = np.zeros(size, dtype=np.uint8)

y = 0
for j in yvector:
    for i in range(xcount):
        img = cv2.imread('../training/'+j+'/'+j+'('+str(i)+').png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
        im_bw = cv2.bitwise_not(img)
        x = i * xbox
        dataset[y:y+im_bw.shape[0], x:x+im_bw.shape[1]] = im_bw
    y = y+ybox

cv2.imwrite('../tmp/dataset.png', dataset)

gray = dataset
# Now we split the image to 5000 cells, each 20x20 size
# cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]
# split the image to 'size' cells, each 'xbox'x'ybox' size
cells = [np.hsplit(row,xcount) for row in np.vsplit(gray,ycount)]

# Make it into a Numpy array. It size will be ('xcout','ycount','xbox','ybox') #(50,100,20,20)
x = np.array(cells)

# Now we prepare train_data and test_data.
#train = x[:,:50].reshape(-1,400).astype(np.float32) # Size = (2500,400)
#test = x[:,50:100].reshape(-1,400).astype(np.float32) # Size = (2500,400)
train = x[:,:xcount/2].reshape(-1,xbox*ybox).astype(np.float32) # Size = (xcout*ycount/2,xbox*ybox)
test = x[:,xcount/2:xcount].reshape(-1,xbox*ybox).astype(np.float32) # Size = (xcout*ycount/2,xbox*ybox)

# Create labels for train and test data
#k = np.arange(10)
k = np.arange(ycount)
# train_labels = np.repeat(k,250)[:,np.newaxis]
train_labels = np.repeat(k,xcount/2)[:,np.newaxis]
test_labels = train_labels.copy()

# Initiate kNN, train the data, then test it with test data for k=1
knn = cv2.KNearest()
knn.train(train,train_labels)
ret,result,neighbours,dist = knn.find_nearest(test,k=5)

# Now we check the accuracy of classification
# For that, compare the result with test_labels and check which are wrong
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print accuracy
'''
# save the data
np.savez('../training/knn_data.npz',train=train, train_labels=train_labels)

# Now load the data
with np.load('../training/knn_data.npz') as data:
    print data.files
    train = data['train']
    train_labels = data['train_labels']
'''

box = np.zeros([ybox, xbox], dtype=np.uint8)
img = cv2.imread('../training/2/2(0).png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
im_bw = cv2.bitwise_not(img)
box[:im_bw.shape[0], :im_bw.shape[1]] = im_bw
test = box.reshape(1,xbox*ybox).astype(np.float32)
ret,result,neighbours,dist = knn.find_nearest(test,k=5)

print ret,result,neighbours,dist