from wait_for_pitch_function import *
from handle_countdown import *
from swing_function import *
from helper_functions import *
from Hack112_A import *

def runPitch():
    cap = cv2.VideoCapture(0)
    # https://stackoverflow.com/questions/19448078/python-opencv-access-webcam-maximum-resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        endEarly = waitUntilReadyToPitch(cap)
        if endEarly:
            cv2.destroyAllWindows()
            return None, None
        startX, startY = beginCountdown(cap)
        #print(startX, startY)
        endX, endY, w, h = swing(startX, startY, cap)
        if startX == None or startY == None or endX == None or endY == None:
            continue
        # time.sleep(2)
        d = distance(startX, startY, endX, endY)
        #print(d)
        xRatio = d/w
        yRatio = endY/h
        if 0.1 <= xRatio < 0.7: # function of distance
            cv2.destroyAllWindows()
            return (getBallContactPoint(xRatio), 1-yRatio)
        elif xRatio >= 0.7: # max swing
            cv2.destroyAllWindows()
            return (0, 1-yRatio)
        else:
            continue

# plateDistance, strikeHeight = runPitch()
# print(plateDistance, strikeHeight)