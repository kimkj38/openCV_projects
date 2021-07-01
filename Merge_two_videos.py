import cv2

video1 = cv2.VideoCapture('hansung.mp4')
video2 = cv2.VideoCapture('video1.mp4')

w = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fps = video1.get(cv2.CAP_PROP_FPS)
delay = int(1000/fps)

out = cv2.VideoWriter('./assignment.avi', fourcc, fps, (w,h))

while True:
    ret1, frame1 = video1.read() #1280x720
    cv2.imshow('Monkey in Hansung', frame1)
    time = video1.get(cv2.CAP_PROP_POS_MSEC)

    if time>3000:
        ret2, frame2 = video2.read()
        if ret2 == True:
            frame2 = cv2.resize(frame2, (320, 240))
            frame1[0:240, 1280-320:1280, :] = frame2
            cv2.imshow('Monkey in Hansung', frame1)

    out.write(frame1)

    if cv2.waitKey(delay) == 27:
      break
cv2.destroyAllWindows()


