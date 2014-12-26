import cv2
import numpy as np
import os.path


class Classification:
    def __init__(self):
        # box with note
        self.xbox = 100#70
        self.ybox = 100#160
        # number pattern and count
        self.xcount = 220
        self.yvector = ['#', 'b', '1', '2', '4', '8', '16', 'k', 'o', 'p', 'p4', 'p8', 'p16', 't', 'pnt',
                        'tnc', 't2', 't3', 't4', 't34', 't68', 'tc']
        self.ycount = len(self.yvector)
        self.knn = cv2.KNearest()
        # train from knn_data.npz prepared file
        if os.path.exists('knn/knn_data.npz'):
            with np.load('knn/knn_data.npz') as data:
                train = data['train']
                train_labels = data['train_labels']
                self.knn.train(train, train_labels)
        elif os.path.exists('knn/dataset.png'):
            # train from image dataset.png
            gray = cv2.imread('knn/dataset.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
            cells = [np.hsplit(row, self.xcount) for row in np.vsplit(gray, self.ycount)]
            x = np.array(cells)
            train = x[:, :3 * self.xcount / 4].reshape(-1, self.xbox * self.ybox).astype(
                np.float32)  # Size = (xcout*ycount/2,xbox*ybox)
            test = x[:, 3 * self.xcount / 4:self.xcount].reshape(-1, self.xbox * self.ybox).astype(
                np.float32)  # Size = (xcout*ycount/2,xbox*ybox)
            k = np.arange(self.ycount)
            train_labels = np.repeat(k, 3 * self.xcount / 4)[:, np.newaxis]
            test_labels = np.repeat(k, self.xcount / 4)[:, np.newaxis]
            self.knn.train(train, train_labels)
            ret,result,neighbours,dist = self.knn.find_nearest(test,k=5)
            matches = result==test_labels
            correct = np.count_nonzero(matches)
            accuracy = correct*100.0/result.size
            print 'accuracy', accuracy, '%'
        else:
            print "ERROR: not found files knn_data.npz or dataset.png need for classifier!"

    # classify image
    def classify(self, img):
        box = cv2.bitwise_not(cv2.resize(img,(100,100)))
        #image_bw = cv2.bitwise_not(img)
        #box = np.zeros([self.ybox, self.xbox], dtype=np.uint8)
        #box[:image_bw.shape[0], :image_bw.shape[1]] = image_bw
        test = box.reshape(-1, self.xbox * self.ybox).astype(np.float32)
        ret, result, neighbours, dist = self.knn.find_nearest(test, k=10)

        # print ret,result,neighbours,dist
        # print ret,yvector[int(ret)], dist[0][0]
        return self.yvector[int(ret)], dist[0][0]