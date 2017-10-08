import os
import cv2
import sys
import time
import os.path

def process(basePath):
    keyframes = os.listdir(basePath + 'keyframes')
    keyframes.sort()
    max = -1
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    for imageFile in keyframes:
        detect(basePath + "keyframes/", imageFile)
        if max == 0:
            break
        max -= 1


def detect(path, file, cascade_file="./lbpcascade_animeface.xml"):
    filename = path + file
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(24, 24))
    matches = False
    face_num = 0
    for (x, y, w, h) in faces:
        matches = True
        face = image[y:y + h, x:x + w]
        cv2.imwrite(path + "../faces/" + str(face_num) + "." + file, face)
        face_num += 1
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)



    if matches:
        cv2.imwrite(path + "../withMatch/" + file, image)

    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
    cv2.imshow('image', image)
    cv2.waitKey(50)