import cv2 as cv
import sys

#find the image
img = cv.imread(cv.samples.findFile("camaro.jpg"))
#check it isn't null
if img is None:
    sys.exit("Could not read the image.")
#show Image
cv.imshow("Camaro zl1 2024", img)
#hold image until user press a key
k = cv.waitKey(0)
#if the pressed key was 'S' write image as new file
if k == ord("s"):
    cv.imwrite("new_camaro.jpg", img)