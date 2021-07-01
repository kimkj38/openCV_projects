import cv2

#데이터 불러오기
src = cv2.imread('find_wally.jpg', cv2.IMREAD_GRAYSCALE)
templ = cv2.imread('wally.png',cv2.IMREAD_GRAYSCALE)

#템플릿과 src의 유사도를 측정한다
res = cv2.matchTemplate(src, templ, cv2.TM_CCOEFF_NORMED)
#0-255 사이의 값으로 grayscale 이미지가 추출되어야 하므로 정규화한다
res_norm = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

#최소값, 최대값, 최소지점, 최대지점을 반환한다
minv, maxv, minloc, maxloc = cv2.minMaxLoc(res)

#TM_CCOEFF_NORMED를 사용했으므로 최댓값을 이용한다
print('maxv:', maxv)
print('maxloc:', maxloc)

#템플릿의 높이와 너비
th, tw = templ.shape[:2]
#그리기 함수 사용을 위해 컬러영상으로 변환
dst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
#pt1과 pt2를 설정하여 매칭하는 곳에 사각형을 그려준다
cv2.rectangle(dst, maxloc, (maxloc[0] + tw, maxloc[1] + th), (0,0,255), 2)

cv2.imshow('res_norm', res_norm)
cv2.imshow('dst', dst)
cv2.waitKey()
cv2.destroyAllWindows()