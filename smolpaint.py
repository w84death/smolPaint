# smolPainter
# by Krzysztof Krystian Jankowski
# (c) 2023/07

import machine
import neopixel
import utime

class smolPaint():
    def __init__(self):
        self.pixels = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.logo = [0,0,0,25,25,25,25,25,25,25,25,25,25,25,25,0,0,0,25,25,25,0,0,0,25,25,25,0,0,0,0,0,0,25,25,25,25,25,25,25,25,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,0,25,0,25,0,0]
        print("\033[7msmolPaint\033[0m started. Use transfer() to push new image.")
        self.draw_bitmap(self.logo)
        utime.sleep(1)

    def update_pixels(self,pixel_string):
        pixel_values = pixel_string.split(',')
        for i in range(25):
            r = int(pixel_values[i*3])
            g = int(pixel_values[i*3 + 1])
            b = int(pixel_values[i*3 + 2])
            self.pixels[24-i] = (r, g, b)
        self.pixels.write()

    def transfer(self):
        print("smolPaint: \033[7mSingle image mode\033[0m.\nInput pixels color stream")
        self.draw_bitmap(self.logo)
        while True:
            data = input("25xR,G,B > ")
            if len(data.split(','))==25*3:
                self.update_pixels(data)
            else:
                print("Wrong data. 25*3 (r,g,b,) expected, got:",len(data.split(',')),data)

    def animator(self):
        print("smolPaint: \033[7mAnimator mode\033[0m.\nPaste frames. Hit enter (empty) to preview animation.")
        self.draw_bitmap(self.logo)
        frames=[]
        current_frame=0
        while True:
            data = input("25xR,G,B > ")
            if data=="":
                for frame in frames:
                    self.update_pixels(frame)
                    utime.sleep(0.1)
            if data=="clear":
                frames=[]
            else:
                if len(data.split(','))==25*3:
                    frames.append(data)
                    for frame in frames:
                        self.update_pixels(frame)
                        utime.sleep(0.1)
                else:
                    print("Wrong data. 25*3 (r,g,b,) expected, got:",len(data.split(',')),data)

    def draw_bitmap(self,bitmap):
        for i in range(25):
            r = int(bitmap[i*3])
            g = int(bitmap[i*3 + 1])
            b = int(bitmap[i*3 + 2])
            self.pixels[24-i] = (r, g, b)
        self.pixels.write()
        
    def gallery(self):
        bitmaps = []
        # apple
        bitmaps.append([0,0,0,0,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,0,27,16,1,27,16,1,20,0,0,0,0,0,11,24,1,0,16,1,33,0,0,33,0,0,11,24,1,0,0,0,33,0,0,33,0,0,20,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3,0,0])
        # cherry
        bitmaps.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,0,25,25,0,16,0,0,0,0,0,0,9,19,1,0,12,1,25,0,11,25,0,16,9,19,1,0,0,0,20,0,16,25,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        # debian
        bitmaps.append([0,0,0,25,0,0,25,0,0,25,0,0,0,0,0,25,0,0,0,0,0,0,0,0,0,0,0,25,0,0,25,0,0,0,0,0,6,0,0,6,0,0,0,0,0,25,0,0,0,0,0,2,0,0,25,0,0,0,0,0,0,0,0,25,0,0,25,0,0,0,0,0,0,0,0])
        
        print("smolPaint: \033[7mGallery mode\033[0m.")
        for pic in bitmaps:
            self.draw_bitmap(pic)
            utime.sleep(1)
            
sp = smolPaint()
sp.gallery()
sp.transfer()


