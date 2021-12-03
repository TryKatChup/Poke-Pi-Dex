import os
from multiprocessing.dummy import Pool as ThreadPool
import argparse
from glob import glob
import numpy as np
import cv2
from common import splitfn


def calibrate_camera(
        input_folder: str,
        square_size: float,
        threads: int,
        output_folder: str):
    """
    Camera calibration for distorted images with chess board samples.
    Reads distorted images, calculates the calibration and write undistorted images

    Usage:
        calibrate_camera(input_folder, sz, threads, output_folder)

    """

    # Store all image names from the specified folder in img_names
    img_names = glob(input_folder + '/*.jpg')
    # If there is no output_folder, simply create a new one
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    # We have a chessboard with 9 x 6 squares.
    # Number of inner corner: number of intersections of squares (8 x 5).
    pattern_size = (8, 5)
    # Get for each point in the grid the i,j indices
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    # Multiply these indices by square size to get real 3D x,y coordinates
    pattern_points *= square_size

    obj_points = []
    img_points = []
    # Images must be loaded grayscale
    h, w = cv2.imread(img_names[0], cv2.IMREAD_GRAYSCALE).shape[:2]  # TODO: use imquery call to retrieve results

    # Process each image from input_dir
    def processImage(fn):
        print('Processing %s... ' % fn)
        image = cv2.imread(fn, 0)
        if image is None:
            print("Failed to load", fn)
            return None

        assert w == image.shape[1] and h == image.shape[0], ("Size: %d x %d ... " % (image.shape[1], image.shape[0]))
        # Detect corners 2D coordinate in the image.
        # Found will be true only if 8x5 image corners will be detected in the image.
        # If the image is too dark or too bright the algorithm may fail detecting corners and found would be false.
        found, chess_corners = cv2.findChessboardCorners(image, pattern_size)
        if found:
            # Refining corner position to subpixel iteratively until criteria
            # max_count=30 or criteria_eps_error=1 is satisfied
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            # Image corners
            cv2.cornerSubPix(image, chess_corners, (5, 5), (-1, -1), term)

        # Save chessboard with drawn corners in output_folder
        vis = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.drawChessboardCorners(vis, pattern_size, chess_corners, found)
        _path, name, _ext = splitfn(fn)
        out_chess = os.path.join(output_folder, name + '_chess.png')
        cv2.imwrite(out_chess, vis)

        if not found:
            print('Chessboard not found')
            return None

        print('           %s... OK' % fn)
        return chess_corners.reshape(-1, 2), pattern_points

    threads_num = int(threads)
    if threads_num <= 1:
        chessboards = [processImage(fn) for fn in img_names]
    else:
        # Multithreaded chessboard image processing
        print("Run with %d threads..." % threads_num)
        pool = ThreadPool(threads_num)
        chessboards = pool.map(processImage, img_names)
    # Process each chessboard image
    chessboards = [x for x in chessboards if x is not None]
    for (corners, pattern_points) in chessboards:
        img_points.append(corners)
        obj_points.append(pattern_points)

    # This method takes as input the corresponding points and the width and height of the image
    # and returns all the parameters of the camera
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
    # - RMS (root mean square error): re-projection error in pixel using the estimated camera parameters.
    #    The lower it is, the better calibration will be obtained. Usually [0.1 - 1] range is good calibration.
    # - camera_matrix: Intrinsics parameters of the camera expressed as 3x3 matrix
    # - dist_coefs: lens distortion coefficients expressed as 1x5 array
    # - rvecs: rotations of the cameras for each chessboard image (Nx3 array)
    #   N: number of images where the chessboard was found during calibration;
    #   3: number of Depth of Field of the rotations.
    # tvecs: translations of the cameras for each chessboard image (Nx3 array).
    #   N: same as before;
    #   3: are coordinates of 3D translation vectors.

    print("\nRMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("distortion coefficients: ", dist_coefs.ravel())

    # undistort the image with the calibration
    print('')
    # For every image used for calibration:
    for fn in img_names:
        # Get path, name and extension of the image
        path, name, ext = splitfn(fn)
        # Save the undistorted image version into output_folder
        img_found = os.path.join(output_folder, name + '_chess.png')
        outfile = os.path.join(output_folder, name + '_undistorted.png')

        img = cv2.imread(img_found)
        if img is None:
            continue

        h, w = img.shape[:2]
        # Undistort an image
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))
        dst = cv2.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)

        # crop and save the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]

        print('Undistorted image written to: %s' % outfile)
        cv2.imwrite(outfile, dst)

    print('Done')


def main():
    # Construct argument parser and add arguments to it
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-s",
        "--square_size",
        required=False,
        type=float,
        default=2.82,
        help="Output folder in which images will be saved (default 2.82)",
    )
    ap.add_argument(
        "-t",
        "--threads",
        type=int,
        required=False,
        default=4,
        help="Number of threads (default 4)",
    )
    ap.add_argument(
        "-i",
        "--input_dir",
        required=True,
        help="Folder with all samples required for calibration",
    )
    ap.add_argument(
        "-o",
        "--output_dir",
        required=False,
        default='./output/',
        help="Folder with info about calibration (default ./output/)",
    )
    args = vars(ap.parse_args())
    calibrate_camera(args["input_dir"], args["square_size"], args["threads"], args["output_dir"])


if __name__ == '__main__':
    print(__doc__)
    main()
    cv2.destroyAllWindows()

