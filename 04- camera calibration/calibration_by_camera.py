import numpy as np
import cv2 as cv
import yaml

# Get corners of the chessboard
print("\nPlease input the pattern size of the chessboard by two integer numbers:")
hc = int(input("Input horizontal squares:"))
hc -= 1
vc = int(input("Input vertical squares:"))
vc -= 1
if hc < 5 or vc < 5:
    exit()


def calibrate_camera_and_show(pattern_size=(hc, vc), capture_device=0):
    cap = cv.VideoCapture(capture_device)

    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images
    objpoints = []  # 3D points in real-world space
    imgpoints = []  # 2D points in the image plane.

    # Criteria for termination of the iterative process of corner refinement
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    found = 0
    print("Put the chessboard on the front of the camera")

    # It's possible to change this number in order to have better experience for scan the chessboard
    while found < 10:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting.")
            break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv.findChessboardCorners(gray, pattern_size, None)

        # If found, draw and add object points, image points (after refining them)
        if ret:
            cv.drawChessboardCorners(frame, pattern_size, corners, ret)
            # Find the exact corner positions
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners2)
            found += 1

        flipVertical = cv.flip(frame, 1)
        cv.imshow('Put chessboard in the front of camera', flipVertical)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

    if found == 10:
        # Calibrate the camera
        (
            ret,  # retval(returns the root mean square (RMS) re-projection error, usually it should be between 0.1
            # and 1.0 pixels in a good calibration.)
            mtx,  # Camera matrix
            dist,  # Distortion coefficients
            rvecs,  # Rotation vectors
            tvecs  # Translation vectors
        ) = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        return ret, mtx, dist, rvecs, tvecs
    else:
        return None, None, None, None, None


ret, mtx, dist, rvecs, tvecs = calibrate_camera_and_show()
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
