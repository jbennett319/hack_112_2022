# necessary imports
import cv2
import mediapipe as mp
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.3,
                      min_tracking_confidence=0.3)
mpDraw = mp.solutions.drawing_utils

# returns the image and hand data from a cap
def readScreen(cap):
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert to proper color format
    results = hands.process(imgRGB)
    # access the hand data
    handData = results.multi_hand_landmarks
    return img, handData

# gets the hand point on screen from all of hand data
def getHandPoint(handData, img):
    handLms = handData[0]
    lm = list(handLms.landmark)[9] # get desired point on hand
    h, w, c = img.shape
    cx, cy = int(w*lm.x), int(h*lm.y)
    return cx, cy

# return True if we are ready for pitch
def readyToPitch(pos, img):
    cx, cy = pos
    h, w, c = img.shape
    readyX, readyY = int(0.8*w), int(0.8*h)
    if cx > readyX and cy > readyY:
        return True
    else:
        return False

def distance(x1, y1, x2, y2):
    result = ((x2-x1)**2 + (y2-y1)**2)**0.5
    return int(result)

def getBallContactPoint(ratio):
    slope = 1/6
    intercept = -7/6
    plateRatio = slope * ratio + intercept
    return plateRatio * 17/12 # convert to feet