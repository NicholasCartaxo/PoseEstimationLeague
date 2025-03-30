import cv2
import mediapipe as mp
import time


class poseDetector():
    def __init__(self, mode=False, complexity=1, smooth=True, segmentation=False,
                  smoothSegmentation=True, detectCon=0.5, trackCon=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.segmentation = segmentation
        self.smoothSegmentation = smoothSegmentation
        self.detectCon = detectCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.segmentation,
                                     self.smoothSegmentation, self.detectCon, self.trackCon)


    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img


    def findPosition(self, img):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        return lmList


    def circle(self, img, detector, id):
        lmList = detector.findPosition(img)
        cx, cy = lmList[id][1], lmList[id][2]
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)




def main():

    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0

    detector = poseDetector(complexity=0)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 3)

        img = detector.findPose(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[0])
            detector.circle(img, detector, 0)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (65, 214, 11), 4)

        cv2.imshow("image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()