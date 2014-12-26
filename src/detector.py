import cv2
from knn.knn_classification import Classification
from note_head_detector import NoteHeadDetector

__author__ = 'Marek'


def detect(staff_finder, symbol_extractor, image_without_staff_lines):
    """
        fixme: pouze vyextrahovana metoda, signatura by mela byt uplne jina. detektor by mel byt asi trida
            Detector
                classify (objects:list) -> labels:list
                train(objects:list, labels:list) nebo train(labeled_objects:list)

            classify funguje asi nejak nasledovne
                pokud nas detekovaci algoritmus umi i noty tak to proste zdetekuje
                pokud ne:
                    zkusi sadu rozdelit na dve kategorie symboly, noty. Na to se muze pouzit nejaky blby zpusob, treba
                    jako ten co je v note_head_detector (nerika jaka je to nota, jenom jestli to je nota).
                    klasifikace pak pokracuje zvlast pro noty zvlast pro ostatni symboly
    """
    #note_detect = NoteHeadDetector(staff_finder.space_height,
    #                               cv2.imread("../resources/black_head2.png", cv2.IMREAD_GRAYSCALE))
    # train KNearestNeighbour
    knn = Classification()
    # trying classification
    i = 0
    for group in symbol_extractor.bounding_groups:
        i += 1
        box = group[0]
        symbol = image_without_staff_lines[box.bottom:box.top, box.left:box.right]
        """
        if symbol.shape[0] > knn.ybox or symbol.shape[1] > knn.xbox:
            refx = -11
            count = 0
            listrefx = []
            for rect in note_detect.heads(symbol):
                listrefx.append(rect.x)
            if not listrefx:
                continue
            listrefx.sort()
            for x in listrefx:
                if abs(refx - x) > 10:
                    count += 1
                    refx = x
            width = symbol.shape[1] / count
            # print width , count , symbol.shape[1], note_detect.heads(symbol)
            startx = 0
            for k in range(width, symbol.shape[1], width):
                sym = symbol[:, startx:k]
                what, distance = knn.classify(sym)
                print 'co,x,y,vzdalenost(0=ok):', what, box.bottom, box.left + startx, distance
                file_name = what + '_' + str(i) + '_' + str(k)
                if distance == 0.0:
                    file_name = 'ok_' + file_name
                cv2.imwrite("..\\tmp\\" + file_name + ".png", sym, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                startx = k
            continue
        """
        what, distance = knn.classify(symbol)
        print 'co,x,y,vzdalenost(0=ok):', what, box.bottom, box.left, distance
        file_name = what + '_' + str(distance) + '_' + str(i)
        if distance == 0.0:
            file_name = 'ok_' + file_name
        cv2.imwrite("..\\tmp\\" + file_name + ".png", symbol, [int(cv2.IMWRITE_JPEG_QUALITY), 90])