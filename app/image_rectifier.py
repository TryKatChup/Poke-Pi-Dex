import cv2
import numpy as np


def rectify_image(img):
    camera_matrix = np.load("./resources/rectification_parameters/camera_matrix.npy")
    dist_coefs = np.load("./resources/rectification_parameters/distortion_coefficients.npy")

    h, w = img.shape[:2]

    # Undistort the image
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))
    dst = cv2.undistort(img, camera_matrix, dist_coefs, None, new_camera_matrix)

    # Crop and Return the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]

    return dst


def rectify_image_from_file(filename):
    img = cv2.imread(filename)
    if img is None:
        print("Rectifier error: image '" + str(img) + "' not found.")
        return

    dst = rectify_image(img)

    # Save to file
    cv2.imwrite(filename[:-4] + "_undistorted.jpg", dst)

    return dst


# Test
if __name__ == "__main__":
    rectify_image("frame.jpg")


