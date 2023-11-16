import cv2 as cv
#read the file
cap = cv.VideoCapture('camaro.mp4')
while cap.isOpened():
    ret, frame = cap.read()
# if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    cv.imshow('frame', gray)
#if user press q do exit
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()