from stereo_camera.network_agent import ImageReceiver
import cv2
import zmq
import sys
import argparse
import typing

# Ports of the sensors
IMG_PORT: int = 8000
CTRL_PORT: int = 8001


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-ip", "--ip_addr", required=True, help="hostname of the sensor"
    )
    args = vars(ap.parse_args())
    ip_addr = args["ip_addr"]
    receiver = ImageReceiver(ip_addr, IMG_PORT, CTRL_PORT)
    receiver.send_sig(b"STREAM")
    sig = receiver.recv_sig()
    # debug
    print(sig)
    receiver.send_sig(b"START")

    while True:
        timestamp, frame = receiver.recv_frame()
        cv2.imshow("Test", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            receiver.send_sig(b"stop")
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
