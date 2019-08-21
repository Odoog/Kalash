from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')

import datetime
import cPickle as pickle
import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import matplotlib.pyplot as plt
import time
import socket
import struct
import json

#constans

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

DELTA = 5
TRESH = 0
TARGET_OBJ = 'person'
COLOR = [255,0,0]
DETECT_TIME = 13

#globals
iteration = DETECT_TIME
bbox, label, conf = [], [], []



Builder.load_string('''
<Main>:
    padding : 30
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: True
    Image:
        id: buf
        source: '3.jpg'
        size: self.texture_size
''')


p1 = '1.jpg'
p2 = '2.jpg'

def deb(message):
    global debugF
    if message != "n":
       debugF.write(str(datetime.datetime.now().time()) + " : " + message + "\n")
    else:
       debugF.write("\n")

class ServerBellhopClass:

    def connecty(self, adress, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((adress, port))

    def send(self, image):

        self.connecty('192.168.1.52', 9098)

        message = json.dumps(image, encoding = "latin1")

        print("len ------------------- ", len(message))

        send_msg(self.sock, message)

        data = recv_msg(self.sock)

        data = json.loads(data.decode("latin1"))

        data[3] = np.asarray(data[3])

        self.sock.close()

        return data[0], data[1], data[2], data[3] #bbox, label, conf, image_array

ServerBellhop = ServerBellhopClass()


debugF = open("debug.txt", 'w')

def change_pic(pic, lout):

    global iteration

    deb("Change_pic enter")

    if lout.ids['camera'].texture != None:

        pixels = lout.ids['camera'].texture.pixels

        pixelsList = list(pixels)

        deb("Start convert pixels")

        for num, item in enumerate(pixelsList):
            pixelsList[num] = struct.unpack('>B', item)

        deb("End convert pixels")

        deb("Start creating output image")

        output_image = np.array(pixelsList, dtype=np.uint8).reshape(480,640,4)[:,:,:3]

        deb("End creating output image")

        # <- output image

        global bbox, label, conf
        #img = cv2.GaussianBlur(img,(15,15),0)
        #if iteration % DETECT_TIME == 0:

        #    bbox, label, conf, output_image = ServerBellhop.send((lout.ids['camera'].texture.pixels, True))
            #log_of_detction
            #print(label, conf)
        #else:
        #    
        #     output_image = ServerBellhop.send((lout.ids['camera'].texture.pixels, False))
        iteration+=1
#       output_image = draw_bbox(img, bbox, label, conf)
        #for i in range(len(conf)):
        #    if label[i] == TARGET_OBJ and conf[i] >= TRESH:
        #        output_image[bbox[i][1] - DELTA : bbox[i][1] + DELTA , bbox[i][0] : bbox[i][2]] = np.array(COLOR, dtype=np.uint8)
        #        output_image[bbox[i][3] - DELTA : bbox[i][3] + DELTA , bbox[i][0] : bbox[i][2]] = np.array(COLOR, dtype=np.uint8)
        #        output_image[bbox[i][1] : bbox[i][3] , bbox[i][0] - DELTA : bbox[i][0] + DELTA] = np.array(COLOR, dtype=np.uint8)
        #        output_image[bbox[i][1] : bbox[i][3] , bbox[i][2] - DELTA : bbox[i][2] + DELTA] = np.array(COLOR, dtype=np.uint8)

        # -> output image

        deb("Start update texture")

        image_texture = Texture.create(
            size=(output_image.shape[1], output_image.shape[0]), colorfmt='rgb')
        image_texture.blit_buffer(output_image.tostring(), colorfmt='rgb', bufferfmt='ubyte')
        pic.texture = image_texture

        deb("End update texture")
        deb("n")

    Clock.schedule_once(lambda _: change_pic(pic, lout), 0)

    
class Main(BoxLayout):
    def reloading(self):
        self.ids['buf'].source = '1.jpg'
    def reloading2(self):
        self.ids['buf'].source = '2.jpg'
    pass

class WEEDEO(App):
    def build(self):
        blt = Main()
        change_pic(blt.ids['buf'], blt)
        return blt



WEEDEO().run()
