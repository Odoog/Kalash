from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')

import pickle
import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import matplotlib.pyplot as plt
%matplotlib inline
import time
import socket
import struct

#constans

DELTA = 5      #Половина толщины рамки в пикселях
TRESH = 0    #Трешхолд, степень уверенности, начиная с которой объекты выделяются, д.ед
TARGET_OBJ = 'person' #целевой объект 
COLOR = [255,0,0]     #цвет рамки, RGB
DETECT_TIME = 13       #n, обновление рамки проиходит каждые n кадров 

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

class ServerBellhopClass:

    def __init__(self, adress, port):

        self.sock = socket.socket()
        self.sock.connect((port, adress))

        sock.close()

        print(data)

    def send(image):

    image = pickle.loads(data)

        message = pickle.dumps(image)
        self.sock.send(message)

        data = self.sock.recv(1024)

        data = pickle.loads(data)

        return data[0], data[1], data[2] #bbox, label, conf

ServerBellhop = ServerBellhopClass('localhost', 9090)


def change_pic(pic, lout):
    if lout.ids['camera'].texture != None:
        output_image = np.array(list(lout.ids['camera'].texture.pixels), dtype=np.uint8).reshape(480, 640, 4)[:,:,:3]

        # <- output image

        global bbox, label, conf
        global iteration
        #img = cv2.GaussianBlur(img,(15,15),0)
        if iteration % DETECT_TIME == 0:

            bbox, label, conf = ServerBellhop.send(output_image)
            #log_of_detction
            #print(label, conf) 
        iteration+=1
#       output_image = draw_bbox(img, bbox, label, conf)
        for i in range(len(conf)):
            if label[i] == TARGET_OBJ and conf[i] >= TRESH:
                output_image[bbox[i][1] - DELTA : bbox[i][1] + DELTA , bbox[i][0] : bbox[i][2]] = np.array(COLOR, dtype=np.uint8)
                output_image[bbox[i][3] - DELTA : bbox[i][3] + DELTA , bbox[i][0] : bbox[i][2]] = np.array(COLOR, dtype=np.uint8)
                output_image[bbox[i][1] : bbox[i][3] , bbox[i][0] - DELTA : bbox[i][0] + DELTA] = np.array(COLOR, dtype=np.uint8)
                output_image[bbox[i][1] : bbox[i][3] , bbox[i][2] - DELTA : bbox[i][2] + DELTA] = np.array(COLOR, dtype=np.uint8)

        # -> output image

        image_texture = Texture.create(
            size=(output_image.shape[1], output_image.shape[0]), colorfmt='rgb')
        image_texture.blit_buffer(cv2.flip(output_image, 0).tostring(), colorfmt='rgb', bufferfmt='ubyte')
        pic.texture = image_texture
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
