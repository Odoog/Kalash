import time
import socket
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import _pickle as pickle
from cvlib.object_detection import draw_bbox
import struct

TRESH = 0

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 9098))
sock.listen(1)

while True:

    conn, addr = sock.accept()

    data = recv_msg(conn)

    if not data:

        print("len data 1 -------------", len(data))
        continue

    else:

        print("len data 2 -------------", len(data))

        print(data[:100])

        image = pickle.loads(data)

        bbox, label, conf = cv.detect_common_objects(image, confidence=TRESH, model='yolov3-tiny')

        data = pickle.dumps((bbox, label, conf))

        print("answer ------------------")

        send_msg(conn, data)

        conn.close()

conn.close()
