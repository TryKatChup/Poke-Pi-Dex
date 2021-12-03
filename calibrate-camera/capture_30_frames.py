import cv2
import os
import time
import argparse


def capture_sample_images(img_folder: str):
    """Method which captures sample images
    :param img_folder: string representing the path to the folder in which images will be saved"""
    print("Collecting images of a chessboard for calibration...")

    # Initialize variables for countdown
    n_pics, tot_pics = 0, 30
    n_sec, tot_sec = 0, 4
    str_sec = "4321"

    # Define folders where calibration images will be stored
    path = os.path.join(img_folder, "Camera")
    # Start streaming
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # Check if camera was opened correctly
    if not (cap.isOpened()):
        print("Could not open video device")

    # Save start time
    start_time = time.time()
    while True:
        # Get frames from both cameras
        ret, frame = cap.read()
        # Flip frames horizontally to make it more comfortable for humans
        flipped_frame = cv2.flip(frame, 1)

        # Display counter on screen before saving frame
        if n_sec < tot_sec:
            # Draw on screen the current remaining pictures
            cv2.putText(
                img=flipped_frame,
                text=f"{n_pics}/{tot_pics}",
                org=(int(10), int(40)),
                fontFace=cv2.FONT_HERSHEY_DUPLEX,
                fontScale=1,
                color=(255, 255, 255),
                thickness=3,
                lineType=cv2.LINE_AA,
            )

            # If time elapsed is greater than one second, update 'n_sec'
            time_elapsed = time.time() - start_time
            if time_elapsed >= 1:
                n_sec += 1
                start_time = time.time()
        else:
            # When countdown ends, save original grayscale image to file
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(path, f"{n_pics:02d}" + ".jpg"), gray_frame)
            # Update counters
            n_pics += 1
            n_sec = 0

            print(f"\n{n_pics}/{tot_pics} images collected.")

        # If 'q' is pressed, or enough images are collected,
        # termination signal is sent to the sensors and streaming ends
        if (cv2.waitKey(1) & 0xFF == ord("q")) or n_pics == tot_pics:
            # self.multicast_send_sig(b"STOP")
            # self._kill_io_threads()
            break
    cv2.destroyAllWindows()
    print("Images collected.")


def main():
    # Construct argument parser and add arguments to it
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o",
        "--output_dir",
        required=True,
        help="output folder in which images will be saved",
    )

    args = vars(ap.parse_args())
    capture_sample_images(args["output_dir"])


if __name__ == "__main__":
    main()

