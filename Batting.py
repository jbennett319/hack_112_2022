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

def batting(cap, startX, startY, radius):
    while True:
        img, handData = readScreen(cap)
        cv2.imshow("Image", img)
        time.sleep(5)
        img, handData = readScreen(cap)
        if handData:
            endX, endY = getHandPoint(handData, img)
            cv2.circle(img, (endX, endY), radius, (255,0,0), cv2.FILLED)
            #if distance((startX, startY), (endX, endY) > .5:
                #you hit the ball
        #print strike or some bs
        # waitUntilReadyToPitch(cap)