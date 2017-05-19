import cv2
from cross_classify import cross_classify


class CameraSource:
    def __init__(self):

        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.glasses_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

        self.c = cv2.VideoCapture(0)

        self.face_x, self.face_y, self.face_w, self.face_h = 0, 0, 0, 0

    def get_ratio(self):
        val, img = self.c.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_height, img_width, img_channels = img.shape
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        eyes = []
        glasses = []
        if len(faces) > 0:
            old_dims = self.face_x, self.face_y, self.face_w, self.face_h
            self.face_x, face_y, self.face_w, self.face_h = faces[0]
            roi_gray = gray[face_y:face_y + self.face_h, self.face_x:self.face_x + self.face_w]
            roi_color = img[face_y:face_y + self.face_h, self.face_x:self.face_x + self.face_w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            glasses = self.glasses_cascade.detectMultiScale(roi_gray)
            eyes, glasses = cross_classify(eyes, glasses)
            if len(eyes) == 0 and len(glasses) == 0:
                self.face_x, face_y, self.face_w, self.face_h = old_dims
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        for (ex, ey, ew, eh) in glasses:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
        cv2.rectangle(img, (self.face_x, self.face_y), (self.face_x + self.face_w, self.face_y + self.face_h),
                      (255, 0, 0), 2)

        ratio_x = self.face_w / float(img_width)
        ratio_y = self.face_h / float(img_height)

        print("----- DIMS ------")
        print(str(self.face_h) + " / " + str(img_height) + " ::: " + str(self.face_w) + " / " + str(img_width))
        print(str(ratio_y) + " ::: " + str(ratio_x))

        # cv2.imshow('img', img)
        decision = cv2.waitKey(1)
        return (ratio_x + ratio_y) / 2.0
