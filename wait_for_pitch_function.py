# necessary imports
import cv2
import mediapipe as mp
import time
from helper_functions import *

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.3,
                      min_tracking_confidence=0.3)
mpDraw = mp.solutions.drawing_utils

# cap = cv2.VideoCapture(0)

def waitUntilReadyToPitch(cap):
    while True:
        img, handData = readScreen(cap)
        if handData:
            cx, cy = getHandPoint(handData, img)
            pos = (cx, cy)
            radius = 40
            cv2.circle(img, (cx, cy), radius, (255,0,0), cv2.FILLED)
            if readyToPitch(pos, img):
                break
        h, w, c = img.shape
        cv2.rectangle(img,(int(0.8*w),int((0.8*h))),(w,h),(0,0,255),3)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            return True
    return False
