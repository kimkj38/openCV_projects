import cv2
import numpy as np

# 파일을 불러온다.
video1 = cv2.VideoCapture('hansung.mp4')
video2 = cv2.VideoCapture('woman.mp4')

# 오류를 처리한다.
if not video1.isOpened() or not video2.isOpened():
    print('[!] video open failed!')

# 영상 정보의 값을 정의한다.
w = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video1.get(cv2.CAP_PROP_FPS)
delay = int(1000/fps)

# 영상 저장을 위한 코드를 설정한다.
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('./assignment2.avi', fourcc, fps, (w,h))

# video2의 전체 프레임을 total_frames로 정의한다.
total_frames = video2.get(cv2.CAP_PROP_FRAME_COUNT)

while True:
    # video1의 frame을 불러온다.
    ret1, frame1 = video1.read()
    # video2의 현재 프레임을 current_frame으로 정의한다.
    current_frame = video2.get(cv2.CAP_PROP_POS_FRAMES)

    # video2의 영상이 끝날때까지만 합성된 영상을 재생한다.
    if current_frame < total_frames:
        ret2, frame2 = video2.read()
        hsv_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame2, (50, 0, 0), (70, 255, 255)) # 초록색 배경을 추출하여 mask로 정의한다.
        masked_frame = np.copy(frame2)
        masked_frame[mask != 0] = [0, 0, 0] # video2에서 마스크가 아닌 부분의 BGR을 [0, 0, 0]으로 만들어준다.

        background = np.copy(frame1)
        background[mask == 0] = [0, 0, 0] # video1에서 마스크인 부분의 BGR을 [0, 0, 0]으로 만들어준다.

        final_frame = background + masked_frame # 두 영상의 프레임 합쳐준다.
        cv2.imshow('video', final_frame) # 합성된 영상을 재생한다.
        out.write(final_frame) # 합성된 영상을 프레임 단위로 저장한다.

    # video2가 끝난 이후에는 video1만 재생한다.
    else:
        cv2.imshow('video', frame1)
        out.write(frame1)

    if cv2.waitKey(delay) == 27:
        break
cv2.destroyAllWindows()
