import cv2
import numpy as np

src = cv2.imread('warp.jpg') #이미지를 불러온다
w, h = 720, 540 #변환될 크기를 지정한다
red = (0,0,255)
coorlist = [] #좌표값이 들어갈 빈 리스트를 만든

# mouse callback
def mouse_event(event, x, y, flags, param):
  if event == cv2.EVENT_LBUTTONDOWN:
    img = src.copy() #복사본 생성
    coorlist.append([x, y]) #빈 리스트에 마우스 클릭한 좌표값 추가
    for xx, yy in coorlist:
        cv2.circle(img, (xx,yy), 7, red, -1, cv2.LINE_AA) #좌표값을 중심점으로 잡아 반지름이 7인 채워진 빨간원을 그린다
    cv2.imshow('img', img)

# perspective transformation
    if len(coorlist) == 4: #4개의 좌표값을 지정하면 시행
        srcQuad = np.array(coorlist, dtype=np.float32) #좌상, 우상, 우하, 좌하

        #윗변과 아랫변 중 긴 변을 변환될 형태의 너비로 잡는다
        w = max(np.linalg.norm(srcQuad[0] - srcQuad[1]), np.linalg.norm(srcQuad[2] - srcQuad[3]))
        #변과 우변 중 긴 변을 변환될 형태의 높이로 잡는다
        h = max(np.linalg.norm(srcQuad[0] - srcQuad[3]), np.linalg.norm(srcQuad[1] - srcQuad[2]))

        dstQuad = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32) #변환될 형태의 사이즈

        perspect = cv2.getPerspectiveTransform(srcQuad, dstQuad) #원근 투시 변환 행렬 계산
        dst = cv2.warpPerspective(src, perspect, (w, h)) #원근 투시 변환
        cv2.imshow('dst', dst)

cv2.namedWindow('img') #윈도우 생성
cv2.setMouseCallback('img', mouse_event) #마우스 콜백함수 불러오기

cv2.imshow('img', src)
cv2.waitKey(0)
cv2.destroyAllWindows()