import cv2
import time
import PoseModule as pm
import math
import pyautogui
import pydirectinput
import mouse

detector = pm.poseDetector()

cap = cv2.VideoCapture(0)
pTime = 0
cTime = 0

log = 0

Tpose = [[11, 371, 139], [12, 250, 137], [13, 453, 145], [14, 158, 139], [19, 574, 140], [20, 44, 140],
         [23, 338, 320], [24, 271, 317], "Tpose"]

armDown = [[11, 388, 136], [12, 274, 137], [13, 460, 158], [14, 189, 155], [19, 460, 261], [20, 191, 261],
        [23, 361, 322], [24, 295, 322], "armDown"]

armL = [[11, 377, 150], [12, 263, 128], [13, 388, 240], [14, 180, 140], [19, 381, 346], [20, 57, 136],
        [23, 346, 316], [24, 282, 315], "armL"]

armR = [[11, 357, 140], [12, 248, 152], [13, 433, 157], [14, 234, 237], [19, 550, 154], [20, 246, 339],
        [23, 337, 317], [24, 272, 319], "armR"]

dabL = [[11, 389, 155], [12, 298, 147], [13, 396, 147], [14, 204, 150], [19, 277, 135], [20, 85, 158],
        [23, 380, 315], [24, 324, 319], "dabL"]

dabR = [[11, 354, 135], [12, 280, 151], [13, 446, 132], [14, 262, 139], [19, 571, 129], [20, 362, 129],
        [23, 351, 318], [24, 302, 319], "dabR"]

sheshL = [[11, 371, 156], [12, 266, 152], [13, 373, 243], [14, 238, 242], [19, 263, 239], [20, 192, 346],
          [23, 348, 315], [24, 280, 310], "sheshL"]

sheshR = [[11, 356, 157], [12, 250, 150], [13, 388, 244], [14, 254, 223], [19, 436, 337], [20, 366, 233],
          [23, 327, 325], [24, 263, 321], "sheshR"]

cross = [[11, 354, 147], [12, 256, 142], [13, 341, 225], [14, 265, 216], [19, 269, 150], [20, 343, 144],
         [23, 333, 304], [24, 271, 303], "cross"]

crossD = [[11, 367, 147], [12, 261, 145], [13, 366, 230], [14, 256, 229], [19, 270, 291], [20, 348, 306],
          [23, 340, 301], [24, 277, 299], "crossD"]

strong = [[11, 373, 142], [12, 262, 141], [13, 456, 148], [14, 179, 141], [19, 409, 51], [20, 227, 57],
          [23, 354, 326], [24, 289, 326], "strong"]

moves = [Tpose, armDown, armL, armR, dabL, dabR, sheshL, sheshR, cross, crossD, strong]

w, x, y, z = 0, 0, 0, 0


def isCoordClose(id, move):
    cx, cy = coords[id][1], coords[id][2]
    mx, my = move[id][1], move[id][2]

    if math.isclose(cx, mx, abs_tol=50) and math.isclose(cy, my, abs_tol=50):
        return True
    else: return False



def isPose(move):
    if isCoordClose(0, move) and isCoordClose(1, move) and isCoordClose(2, move) and isCoordClose(3, move) and isCoordClose(4, move) and isCoordClose(5, move) and isCoordClose(6, move) and isCoordClose(7, move) == True :
        return move[8]
    else: return "neutral"


def neutralF():
    global w, x, y, z
    if w == 1:
        mouse.release('right')
        pydirectinput.keyUp('shift')
        w = 0

    if x == 1:
        pydirectinput.keyUp('d')
        pydirectinput.keyUp('f')
        x = 0

    if y == 1:
        pydirectinput.keyUp('e')
        pydirectinput.keyUp('r')
        y = 0

    if z == 1:
        pydirectinput.keyUp('q')
        pydirectinput.keyUp('w')
        z = 0


def TposeF():
    global w
    if w == 0:
        pydirectinput.click(683, 170, button='right')
    w = 1

def armDownF():
    global w
    if w == 0:
        pydirectinput.click(683, 560, button='right')
    w = 1

def armLF():
    global w
    if w == 0:
        pydirectinput.click(500, 384, button='right')
    w = 1

def armRF():
    global w
    if w == 0:
        pydirectinput.click(900, 384, button='right')
    w = 1

def dabLF():
    global z
    if z == 0:
        pydirectinput.keyDown('q')
    z = 1

def dabRF():
    global z
    if z == 0:
        pydirectinput.keyDown('w')
    z = 1

def sheshLF():
    global y
    if y == 0:
        pydirectinput.keyDown('e')
    y = 1

def sheshRF():
    global x
    if x == 0:
        pydirectinput.keyDown('r')
    x = 1

def strongF():
    global w
    if w == 0:
        pydirectinput.keyDown('shift')
        pydirectinput.click(button='right')
    w = 1

def crossF():
    global x
    if x == 0:
        pydirectinput.keyDown('d')
    x = 1

def crossDF():
    global x
    if x == 0:
        pydirectinput.keyDown('f')
    x = 1








while True:
    success, img = cap.read()
    img = cv2.flip(img, 3)

    img = detector.findPose(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:

        coords = [lmList[11], lmList[12], lmList[13], lmList[14], lmList[19], lmList[20], lmList[23], lmList[24],]


        whatPose = [isPose(i) for i in moves]

        while len(whatPose) != 1:
            whatPose.remove("neutral")
        whatPose = whatPose[0]

        eval(whatPose + "F()")


        cv2.putText(img, whatPose, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (65, 214, 11), 4)


        # if log != 100:
        #     print(coords)
        #     log = log+1







    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (65, 214, 11), 4)

    cv2.imshow("image", img)
    cv2.waitKey(1)