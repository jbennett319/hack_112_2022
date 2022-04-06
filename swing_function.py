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

def swing(startX, startY, cap):
    timer = 1
    while timer > 0:
        img, handData = readScreen(cap)
        radius = 40
        cv2.circle(img, (startX, startY), radius, (255,0,0), 5)
        if handData:
            cx, cy = getHandPoint(handData, img)
            pos = (cx, cy)
            radius = 40
            cv2.circle(img, (cx, cy), radius, (255,0,0), 5)
        else:
            cx, cy = None, None
        cv2.imshow("Image", img)
        timer -= 0.05
        key = cv2.waitKey(1)
        h, w, c = img.shape
    return cx, cy, w, h