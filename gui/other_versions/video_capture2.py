import cv2
from threading import Thread

class VideoGet:
    def __init__(self, video_source=0):
        self.stream = cv2.VideoCapture(video_source)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = True
        if not self.stream.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def start(self):
        Thread(target=self.get_frame, args=()).start()
        return self

    def get_frame(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True
