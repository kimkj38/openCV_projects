import cv2

#데이터 불러오기
face = cv2.imread('selfie.jpeg')
batman = cv2.imread('batmask.png', cv2.IMREAD_UNCHANGED)

#얼굴 검출 객체 생성
classifier = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt2.xml')
if classifier.empty():
    print('XML load failed!')

#멀티스케일 객체검출
faces = classifier.detectMultiScale(face)
#얼굴 해당 영역의 좌표 리턴
x,y,w,h = faces[0]
print(x,y,w,h)

#관심영역 지정
roi = face[y:y+h, x:x+w]

#가면 사이즈 조정
batman_fit = cv2.resize(batman, (w,h), interpolation=cv2.INTER_LINEAR)

#알파영역 추출하여 마스킹
mask = batman_fit[:, :, 3] #가면이 흰색
batman_fit = batman_fit[:, :, :-1]

#bitwise 연산
mask_inv = cv2.bitwise_not(mask) #가면이 검정
masked_mask = cv2.bitwise_and(batman_fit, batman_fit, mask=mask) #배경이 검정, 가면은 본래 색
masked_roi = cv2.bitwise_and(roi, roi, mask=mask_inv) #roi영역에 가면의 mask 삽입
face[y:y+h, x:x+w] = cv2.add(masked_mask, masked_roi) #덧셈 연산으로 mask에 본래 가면 색 입히기

#cv2.rectangle(face, (x,y,w,h), (0,255,0), 2)

cv2.imshow('face', face)
cv2.waitKey()
cv2.destroyAllWindows()
