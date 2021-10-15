import cv2
from threading import Thread
import tkinter as tk
from PIL import ImageTk, Image


class VideoStreamWidget:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.stopped = False
        self.canvas = None
        # self.thread.daemon = True
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def set_canvas(self, canvas: tk.Canvas):
        self.canvas = canvas

    def start(self):
        Thread(target=self.update_canvas(), args=()).start()
        self.stopped = False
        return self

    def get_frame(self):
        if self.vid.isOpened() and not self.stopped:
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)

    def update_canvas(self):
        ret, frame = self.get_frame()

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame).resize((320, 320), Image.ANTIALIAS))
            self.canvas.create_image(-40, 0, image=self.photo, anchor=tk.NW)

    def stop(self):
        if self.vid.isOpened():
            self.vid.release()