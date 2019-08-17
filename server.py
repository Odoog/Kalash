import time
import socket
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import pickle
from cvlib.object_detection import draw_bbox

TRESH = 0


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 9097))
sock.listen(1)

while True:

    conn, addr = sock.accept()

    time.sleep(0.1)

    data = conn.recv(400000000)

    if not data:

        continue
        print("len data 1 -------------", len(data))

    else:

        print("len data 2 -------------", len(data))
        image = pickle.loads(data)

        bbox, label, conf = cv.detect_common_objects(image, confidence=TRESH, model='yolov3-tiny')

        data = pickle.dumps((bbox, label, conf))

        print("answer ------------------")

        conn.send(data)

        conn.close()

conn.close()
