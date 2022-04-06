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

def beginCountdown(cap):
    timer = 5
    while timer > 0:
        img, handData = readScreen(cap)
        h, w, c = img.shape
        cv2.putText(img, f'Swing in {int(timer)}...', (w//3, h//2), 
            cv2.FONT_HERSHEY_PLAIN, 5, (0,0,255), 3)
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
    return cx, cy