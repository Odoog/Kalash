import socket
import cv2 
import matplotlib.pyplot as plt
import cvlib as cv
import pickle
from cvlib.object_detection import draw_bbox


sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    data = conn.recv(1024)

    if not data:
        continue

    image = pickle.loads(data)

    bbox, label, conf = cv.detect_common_objects(output_image, confidence=TRESH, model='yolov3-tiny')

    data = pickle.dumps((bbox, label, conf))

    conn.send(data)

conn.close()
