from time import sleep

import cv2


from cross_classify import cross_classify

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
glasses_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

c = cv2.VideoCapture(0)

FRAMERATE = 8

decision = 0


x, y, face_w, face_h = 0, 0, 0, 0
while decision != 27:
    val, img = c.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_height, img_width, img_channels = img.shape
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    eyes = []
    glasses = []
    if len(faces) > 0:
        old_dims = x, y, face_w, face_h
        x, y, face_w, face_h = faces[0]
        roi_gray = gray[y:y + face_h, x:x + face_w]
        roi_color = img[y:y + face_h, x:x + face_w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        glasses = glasses_cascade.detectMultiScale(roi_gray)
        eyes, glasses = cross_classify(eyes, glasses)
        if len(eyes) == 0 and len(glasses) == 0:
            x, y, face_w, face_h = old_dims
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    for (ex, ey, ew, eh) in glasses:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
    cv2.rectangle(img, (x, y), (x + face_w, y + face_h), (255, 0, 0), 2)
    print("----- DIMS ------")
    print(str(face_h) + " / " + str(img_height) + " ::: " + str(face_w) + " / " + str(img_width))
    print(str(face_h / float(img_height)) + " ::: " + str(face_w / float(img_width)))

    cv2.imshow('img', img)
    sleep(1.0 / FRAMERATE)
    decision = cv2.waitKey(1)
    # cv2.destroyAllWindows()
