import cv2 as cv
import numpy as np
import glob
import yaml

# Set corners of the chessboard
hc = 9
vc = 6

# Criteria for termination of the iterative process of corner refinement
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points (3D points in real world space)
objp = np.zeros((vc * hc, 3), np.float32)
objp[:, :2] = np.mgrid[0:hc, 0:6].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images
objpoints = []  # 3D point in real world space
imgpoints = []  # 2D points in image plane

# Load images
images = glob.glob('files/*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (hc, vc), None)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv.drawChessboardCorners(img, (hc, vc), corners2, ret)
        cv.imshow("Check images", img)
        cv.waitKey(300)

cv.destroyAllWindows()

# Calibrate the camera
(
    ret,  # retval(returns the root mean square (RMS) re-projection error, usually it should be between 0.1
    # and 1.0 pixels in a good calibration.)
    mtx,  # Camera matrix
    dist,  # Distortion coefficients
    rvecs,  # Rotation vectors
    tvecs  # Translation vectors
) = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

if ret is not None:
    # Show the result and save in the file
    data = {'Camera matrix:': np.asarray(mtx).tolist(), 'Distortion coefficients:': np.asarray(dist).tolist()}
    with open("calibration.yaml", "w") as f:
        yaml.dump(data, f)
    print("The results:\n")
    print("Camera matrix:")
    print(mtx)
    print("\nDistortion coefficients:")
    print(dist)
    print("\n\nAlso you can find this result on the calibration.yaml file")