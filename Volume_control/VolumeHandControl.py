import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript

# 웹캠 연결
cap = cv2.VideoCapture()
cap.open(0)
if not cap.isOpened():
    print('[!]camera open failed!')

# handDetector 객체 생성
detector = htm.handDetector(detectionCon=0.7)

# 초깃값
pTime = 0 # 현재 시간
minVol = 0 # 최소 볼륨
maxVol = 100 # 최대 볼륨
vol = 0 # 현재 볼륨
volBar = 400 # 볼륨바
tipIds = [4, 8, 12, 16, 20] # landmark index
totalFingers = 0 # 펴진 손가락 개수

while True:
    # 비디오를 frame 단위로 저장
    ret, img = cap.read()
    if not ret:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2] # 엄지 끝의 좌표
        x2, y2 = lmList[8][1], lmList[8][2] # 검지 끝의 좌표
        cx, cy = (x1+x2) // 2, (y1+y2) // 2 # 엄지 끝과 검지 끝의 중앙 좌표

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)  # 엄지 끝 좌표에 원 그리기
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)  # 검지 끝 좌표에 원 그리기
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)  # 엄지와 검지 사이 선 그려주기
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)  # 엄지와 검지 중앙 좌표에 원 그리기
        length = math.hypot(x2-x1, y2-y1)  # 엄지와 검지 사이의 거리 계산

        vol = np.interp(length,[30, 300],[minVol, maxVol])  # 30~300의 값을 가지는 length를 0~100 사이의 값으로 mapping
        volBar = np.interp(length, [30, 300], [400, 150])   # 30~300의 값을 가지는 length를 400~150 사이의 값으로 mapping
        #print("length:", int(length), "vol:", vol)

        # length를 통해 구한 vol로 볼륨값 조정
        set_vol = "set volume output volume " + str(vol)
        osascript.osascript(set_vol)

        # vol이 0보다 작으면 가운데 초록색 원 그려주기
        if length < 30:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)


        # 다섯손가락을 전부 편 상태 인식
        fingers = []

        # Thumb
        # 엄지 끝이 엄지의 마디보다 오른쪽에 있으면 1, 왼쪽에 있으면 0
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        # 엄지 제외 네 손가락의 끝이 마디보다 위에 있으면 1, 아래 있으면 0
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # 1로 인식된 손가락의 개수
        totalFingers = fingers.count(1)
        #print(fingers)

    # 볼륨 나타내는 박스 그리기
    cv2.rectangle(img, (50,150), (85,400), (255, 0, 0), 3) # 빈 박스 그리기
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED) # 볼륨에 따라 변하는 채워진 박스 그리기
    cv2.putText(img, f'{int(vol)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3) # 볼륨값 나타내는 text 그리기



    cTime = time.time()  # 현재 시간 저장
    fps = 1 / (cTime - pTime)  # fps 계산
    pTime = cTime  # 현재 시간을 이전 시간으로 갱신

    # fps 화면에 그리기
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                (255, 0, 255), 3)

    # 영상 나타내기
    cv2.imshow("Image", img)

    # esc입력 혹은 다섯손가락을 모두 펴서 종료
    if (cv2.waitKey(30) == 27)|(totalFingers==5):
        break