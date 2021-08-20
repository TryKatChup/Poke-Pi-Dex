import io
import socket
import struct
from PIL import Image
import cv2
import numpy
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) == 3:
    ip_address = sys.argv[1]
    port = int(sys.argv[2])
else:
    ip_address = "192.168.1.88"
    port = 4321
    print("IP address and port missing, will be used default ones")

client_socket.connect((ip_address, port))
connection = client_socket.makefile('rb')
print("Connecting to " + ip_address + ", on port " + str(port) + "...")
try:
    img = None
    while True:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)
        image = Image.open(image_stream)
        im = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        cv2.imshow('Video', im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           print("Video stream terminated")
           break
    cv2.destroyAllWindows()
finally:
    connection.close()
    client_socket.close()
    print("Connection closed")