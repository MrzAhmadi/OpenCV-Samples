import cv2 as cv

# select camera
capture_device = 0
cap = cv.VideoCapture(capture_device)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,  480))

# cap gets every time a frame, so we get frames in an infinite loop
while True:
    ret, frame = cap.read()
# if ret is equals to not it means the access to camera is not possible and let's show error message
    if not ret:
        print("Failed to capture frame. Exiting.")
        break
# the default orientation of frame is flipped, so we flip it to correct way
    flipVertical = cv.flip(frame, 1)
    out.write(flipVertical)
    cv.imshow('Capture Video', flipVertical)
    # hold camera view until user press a key
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()
