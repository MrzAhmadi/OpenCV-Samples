import cv2 as cv

# select camera
capture_device = 0
cap = cv.VideoCapture(capture_device)

# define a value for name counting of images
img_counter = 0

# cap gets every time a frame, so we get frames in an infinite loop
print("Press Space bar to take a image")
while True:
    ret, frame = cap.read()
# if ret is equals to not it means the access to camera is not possible and let's show error message
    if not ret:
        print("Failed to capture frame. Exiting.")
        break
    flipVertical = cv.flip(frame, 1)
    cv.imshow("Capture Image", flipVertical)

    k = cv.waitKey(1)
    if k % 0xFF == ord('q'):
        # Q pressed
        print("Escape hit, closing...")
        break
    elif k % 0xFF == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cap.release()
cv.destroyAllWindows()