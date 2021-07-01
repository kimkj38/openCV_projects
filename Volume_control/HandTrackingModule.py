import cv2
import mediapipe as mp


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # False로 할 경우 첫번째 input image를 tracking하게 되어 비디오에 적합.
        # True로 하면 input image에 대해 매번 detection을 수행한다.
        self.mode = mode
        self.maxHands = maxHands # 인식하는 최대 손 개수
        self.detectionCon = detectionCon # detection에서 Confidence 임계값
        self.trackCon = trackCon # tracking에서의 Confidence 임계값

        self.mpHands = mp.solutions.hands  # 손을 인식하는 모델
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)  # 객체생성
        self.mpDraw = mp.solutions.drawing_utils  # landmarks 그리기 함수

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # RGB로 변환
        self.results = self.hands.process(imgRGB)

        # for문으로 landmark를 하나씩 불러와 그려준다
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # mpHands.HAND_CONNECTIONS: landmark들을 연결
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):

        lmList= [] # landmark list 생성

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):  # 각 landmark의 index와 좌표를 가져온다
                # print(id,lm)
                # lm은 소수점으로 나타나므로 픽셀값이 나오도록 좌표값에 이미지의 width, height를 곱해준다.
                h, w, c = img.shape
                cx, cy, = int(lm.x * w), int(lm.y * h)
                # id, cx, cy로 구성된 리스트를 lmList에 추가한다
                lmList.append([id, cx, cy])

        return lmList
