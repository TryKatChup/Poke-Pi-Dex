import cv2


class VideoCapture:
    def __init__(self, video_source=0):
        self.video_source = video_source
        self.vid = None
        self.width = None
        self.height = None

    def open(self):
        # Open the video source
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", self.video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)

    def close(self):
        if self.vid.isOpened():
            self.vid.release()

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

'''
# Class which uses picamera API (?)
class MyPicameraCapture:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution
'''