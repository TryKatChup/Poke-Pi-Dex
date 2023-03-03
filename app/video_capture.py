import cv2

from video_source_exception import VideoSourceException

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
            raise VideoSourceException("Unable to open video source", self.video_source)

        # Get video source width and height
        # self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Set video source dimensions
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            raise VideoSourceException("Unable to use video source", self.video_source)

    def close(self):
        if self.vid.isOpened():
            self.vid.release()

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid:
            if self.vid.isOpened():
                self.vid.release()


# Test
if __name__ == "__main__":
    vc = VideoCapture(0)
    try:
        vc.open()
        while True:
            ret, frame = vc.get_frame()
            if ret:
                cv2.imshow("Camera Test", frame)
                # Stop when Esc is pressed
                if cv2.waitKey(1) == 27:
                    break
        cv2.destroyAllWindows()
    except Exception as e:
        for arg in e.args:
            print(arg)
