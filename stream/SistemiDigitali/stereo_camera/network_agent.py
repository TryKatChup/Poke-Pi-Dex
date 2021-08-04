import zmq
import imagezmq
import numpy as np
import cv2
import imutils
from imutils.video import VideoStream
import time
import typing

try:
    from picamera import PiCamera

    PICAM: bool = True
except OSError:
    PICAM: bool = False


class NetworkAgent:
    """Class representing a NetworkAgent, able to bind/connect and to communicate over a TCP zmq.PAIR socket.

    Attributes:
        _context -- the ZMQ context underlying the socket
        _sock --- the ZMQ TCP socket over which the communication is performed

    Methods:
        send_sig --- method enabling the sending of a bytes signal over a TCP socket
        recv_sig --- method enabling the reception of a string signal over a TCP socket
        close --- method which releases the network resources used by the object"""

    def __init__(self, port: int, ip_addr: typing.Optional[str] = None):
        """Initialize the NetworkAgent object by setting the ZMQ context, a zmq.PAIR socket and by performing the
        binding to the given port or the connect to the given address and port, depending on the parameters.
            :param port: integer representing the port to which the socket will be bound
            :param ip_addr: optional string representing the ip address to connect to; if set to 'None' (default), the
                            NetworkAgent binds to the given port, otherwise it connects to the given address and port"""

        # Set up context and socket with zero linger time
        self._context: zmq.Context = zmq.Context()
        self._sock: zmq.Socket = self._context.socket(zmq.PAIR)
        self._sock.setsockopt(zmq.LINGER, 0)
        # Perform the bind or the connect depending on the 'ip_addr' parameter
        if ip_addr is None:
            self._sock.bind(f"tcp://*:{port}")
        else:
            self._sock.connect(f"tcp://{ip_addr}:{port}")

    def send_sig(self, sig: bytes, no_block: bool = False):
        """Method implementing the sending of a message over a TCP socket.
        :param sig: bytes representing the signal to be sent
        :param no_block: if set to True, it sends the signal without blocking"""
        flags = zmq.NOBLOCK if no_block else 0
        self._sock.send(sig, flags=flags)

    def recv_sig(self, noblock: bool = False) -> str:
        """Method implementing the reception of a signal over a TCP socket.
        :param noblock: if set to True, it sends the signal without blocking

        :returns a string representing the message received"""
        flags = zmq.NOBLOCK if noblock else 0
        return self._sock.recv_string(flags=flags)

    def close(self):
        """Method that closes the socket and the context to free resources."""
        self._sock.close()
        self._context.term()


class ImageSender(NetworkAgent):
    """Class representing an ImageSender: it inherits from NetworkAgent a zmq.PAIR socket for control signals,
    and it wraps an imagezmq.ImageSender object which enables streaming over a zmq.PUB socket.

    Attributes:
        _sender --- the wrapped ImageSender object which provides method for streaming over a TCP socket
        _streamer --- a VideoStream object which handles image capturing
        _jpeg_quality --- integer representing the quality of the JPEG compression
        _rotate --- a parameter indicating whether to rotate the image before sending it

    Methods:
        send_frame --- method enabling the sending of an OpenCV image/NumPy array over a TCP socket
        stream --- the method implementing the streaming of images which are captured by the device and sent over the
        underlying TCP socket
        close --- method which releases the network resources used by the object"""

    def __init__(
        self,
        stream_port: int,
        ctrl_port: int,
        res: typing.Tuple[int, int],
        framerate: int = 10,
        jpeg_quality: int = 95,
        rotate: bool = False,
    ):
        """Constructor of ImageSender object, which performs the following steps:
        - it sets up a zmq.PAIR socket for control signals by calling the base class NetworkAgent constructor;
        - it wraps and initialize a imagezmq.ImageSender object in PUB/SUB mode;
        - it initializes a VideoStream object with the proper resolution and framerate (using PiCamera if available).
           :param stream_port: integer representing the port to which the socket for the image streaming will be bound
           :param ctrl_port: integer representing the port to which the socket for the control signals will be bound
           :param res: tuple of two ints representing the resolution of the sensor
           :param framerate: integer representing the framerate (by default 10)
           :param jpeg_quality: integer representing the quality of the JPEG compression
           :param rotate: optional boolean, if 'True' the image will be rotated by 180 degrees
                          before being sent (by default it is set to 'False')"""
        # Set up socket for control signals
        super(ImageSender, self).__init__(ctrl_port)

        # Set up ImageSender in PUB/SUB mode
        self._sender = imagezmq.ImageSender(
            connect_to=f"tcp://*:{stream_port}", REQ_REP=False
        )

        # Set sensor options
        self._streamer = (
            VideoStream(usePiCamera=True, resolution=res, framerate=framerate)
            if PICAM
            else VideoStream(src=0, resolution=res, framerate=framerate)
        )
        self._jpeq_quality = jpeg_quality
        self._rotate = rotate

        # Initialize streamer
        self._streamer.start()

    def send_frame(self, frame: np.ndarray):
        """Method implementing the sending of an image over the zmq.PUB socket, together with the timestamp.
        :param frame: the NumPy's array to be sent"""
        _, jpg_frame = cv2.imencode(
            ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), self._jpeq_quality]
        )
        self._sender.send_jpg(time.time(), jpg_frame)

    def stream(self):
        """Method that implements the streaming of images over the zmq.PUB socket."""
        print("Streaming...")

        # Camera warm-up
        time.sleep(2.0)

        # Send ready message to master and wait for the starting signal
        self.send_sig(b"READY")
        sig = self.recv_sig()
        print(f"Master: {sig}")

        while True:
            # Read frame
            frame = self._streamer.read()

            # Rotate image, if specified
            if self._rotate:
                frame = imutils.rotate_bound(frame, angle=180)

            # Send the frame
            self.send_frame(frame)

            # Try to read control signals from a non-blocking recv
            try:
                # If the recv succeeds, check the signal
                sig = self.recv_sig(noblock=True)
                print(f"Master: {sig}")
                if sig == "RESET":
                    print("Resetting the sensor...")
                    # Send ready message to master and wait for the starting signal
                    self.send_sig(b"READY")
                    sig = self.recv_sig()
                    print(f"Master: {sig}")
                else:
                    break
            except zmq.Again:
                pass
        print("Streaming ended.")

    def close(self):
        """Method which releases the resources employed by the object."""
        super(ImageSender, self).close()
        self._sender.close()
        self._streamer.stop()


class ImageReceiver(NetworkAgent):
    """Class representing an ImageReceiver: it inherits from NetworkAgent a zmq.PAIR socket for control signals,
    and it wraps an imagezmq.ImageHub object which enables receiving a stream over a zmq.SUB socket.

    Attributes:
        _receiver --- the wrapped ImageHub object which provides method for receiving a stream over a TCP socket

    Methods:
        recv_frame --- method enabling the receiving of a frame over a TCP socket
        flush_pending_frames --- method flushing the socket from pending frames
        close --- method which releases the network resources used by the object"""

    def __init__(self, ip_addr: str, stream_port: int, ctrl_port: int):
        """Constructor of ImageReceiver object, which performs the following steps:
        - it sets up a zmq.PAIR socket for control signals by calling the base class NetworkAgent constructor;
        - it wraps and initialize a imagezmq.ImageHub object in PUB/SUB mode.
           :param ip_addr: string representing the ip address of the ImageReceiver to connect to
           :param stream_port: integer representing the port to which the socket for the image streaming will be bound
           :param ctrl_port: integer representing the port to which the socket for the control signals will be bound"""
        # Set up socket for control signals
        super(ImageReceiver, self).__init__(ctrl_port, ip_addr)

        # Set up ImageHub in PUB/SUB mode
        self._receiver = imagezmq.ImageHub(
            open_port=f"tcp://{ip_addr}:{stream_port}", REQ_REP=False
        )

    def recv_frame(self) -> (float, np.ndarray):
        """Method implementing the receiving of an image over the zmq.SUB socket, together with the timestamp."""
        tstamp, jpg_frame = self._receiver.recv_jpg()
        frame = cv2.imdecode(
            np.fromstring(jpg_frame, dtype=np.uint8), cv2.IMREAD_UNCHANGED
        )
        return tstamp, frame

    def flush_pending_frames(self):
        """Method that flushes the SUB socket from pending frames."""
        self._receiver.zmq_socket.setsockopt(zmq.RCVTIMEO, 500)
        while True:
            # When recv timeout expires, break from the loop
            try:
                self.recv_frame()
            except zmq.Again:
                break
        self._receiver.zmq_socket.setsockopt(zmq.RCVTIMEO, -1)

    def close(self):
        """Method which releases the resources employed by the object."""
        super(ImageReceiver, self).close()
        self._receiver.close()
