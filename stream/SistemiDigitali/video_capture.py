
from stereo_camera.network_agent import ImageSender
import zmq
import sys
import argparse
import typing

# Ports of the sensors
IMG_PORT: int = 8000
CTRL_PORT: int = 8001

# Camera size and framerate
RES: typing.Tuple[int, int] = (640, 480)


def main():
    # Construct argument parser and add arguments to it
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-fr",
        "--framerate",
        required=False,
        help="frame rate of the sensor (default 10)",
    )
    ap.add_argument(
        "-q",
        "--jpeg_quality",
        required=False,
        help="quality of the JPEG compression (default 95)",
    )
    ap.add_argument(
        "-r",
        "--rotate",
        action="store_true",
        help="if set, image is rotated by 180 degrees before being "
        "sent to master (useful in particular hardware setups)",
    )
    args = vars(ap.parse_args())

    # Argument reading and check
    try:
        framerate = int(args["framerate"]) if args["framerate"] is not None else 10
    except ValueError:
        sys.exit("Framerate must be an integer.")
    try:
        jpeg_quality = (
            int(args["jpeg_quality"]) if args["jpeg_quality"] is not None else 95
        )
    except ValueError:
        sys.exit("JPEG quality must be an integer.")
    if jpeg_quality < 0 or jpeg_quality > 100:
        sys.exit("JPEG quality must be between 0 and 100.")
    rotate = args["rotate"]

    # Create Sensor object
    sender = ImageSender(IMG_PORT, CTRL_PORT, RES, framerate, jpeg_quality, rotate)

    try:
        while True:
            print(f"Waiting on port {CTRL_PORT}...")
            sig = sender.recv_sig()
            print(f"Master: {sig}")
            # Start streaming
            sender.stream()
    except zmq.ZMQError:
        print("\nError communicating over the network.")
    except KeyboardInterrupt:
        print("\nTermination enforced manually.")
    finally:
        # Free resources
        sender.close()
        print("Terminating...")


if __name__ == "__main__":
    main()
