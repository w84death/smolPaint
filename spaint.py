# smolPaint GUI
# Tiny paint program for 5x5 NeoPixel BFF Grid displays
# by Krzysztof Krystian Jankowski
# (c) 2023/07

import machine
import neopixel

class smolPaint():
    def __init__(self):
        self.pixels = neopixel.NeoPixel(machine.Pin(29),5*5)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.logo = "0,0,0,45,41,255,45,41,255,45,41,255,45,41,255,45,41,255,45,41,255,45,41,255,45,41,255,45,41,255,45,41,255,0,0,0,45,41,255,0,0,0,0,0,0,45,41,255,0,0,0,45,41,255,0,0,0,0,0,0,0,0,0,45,41,255,45,41,255,0,0,0,0,0,0"
        print("smolPaint started. Use transfer() to push new image.")
        self.update_pixels(self.logo)

    def update_pixels(self,pixel_string):
        pixel_values = pixel_string.split(',')
        for i in range(25):
            r = int(pixel_values[i*3])
            g = int(pixel_values[i*3 + 1])
            b = int(pixel_values[i*3 + 2])
            self.pixels[24-i] = (r, g, b)
        self.pixels.write()

    def transfer(self):
        print("smolPaint: Input pixels color stream")

        while True:
            data = input("25xR,G,B > ")
            if len(data.split(','))==25*3:
                self.update_pixels(data)
            else:
                print("Wrong data. 25*3 (r,g,b,) expected, got:",len(data.split(',')),data)

sp = smolPaint()
sp.transfer()
