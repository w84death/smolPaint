# smolPainter
# by Krzysztof Krystian Jankowski
# (c) 2023/07

import machine
import neopixel
import utime

# Define constants
PIXEL_COUNT = 25
PIXEL_DIMENSION = 3
NEOPIXEL_PIN = 29

# Define smolPaint class
class smolPaint:
    """
    A class to handle NeoPixel painting operations.
    """
    def __init__(self):
        """
        Initialize the smolPaint object.
        """
        self.pixels = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), PIXEL_COUNT)
        self.pixels.fill((0,0,0))
        self.pixels.write()
        self.logo = [0,0,0,25,25,25,25,25,25,25,25,25,25,25,25,0,0,0,25,25,25,0,0,0,25,25,25,0,0,0,0,0,0,25,25,25,25,25,25,25,25,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,0,25,0,25,0,0]
        print("\033[7msmolPaint\033[0m started. Use transfer() to push new image.")
        self.draw_bitmap(self.logo)
        utime.sleep(1)

    def update_pixels(self, pixel_values):
        """
        Update the NeoPixel grid with new pixel values.
        """
        for i in range(PIXEL_COUNT):
            self.pixels[PIXEL_COUNT-1-i] = tuple(map(int, pixel_values[i*PIXEL_DIMENSION: (i+1)*PIXEL_DIMENSION]))
        self.pixels.write()

    def draw_bitmap(self, bitmap):
        """
        Draw a bitmap on the NeoPixel grid.
        """
        self.update_pixels(bitmap)

    def transfer(self, data):
        """
        Transfer a single image to the NeoPixel grid.
        """
        self.draw_bitmap(self.logo)
        tokens = data.split(',')
        if len(tokens)==PIXEL_COUNT*PIXEL_DIMENSION:
            self.update_pixels(tokens)
        else:
            print("Wrong data. Expected",PIXEL_COUNT*PIXEL_DIMENSION,"tokens (r,g,b) but got:", len(tokens))

    def animator(self, data):
        """
        Animate a sequence of frames on the NeoPixel grid.
        """
        self.draw_bitmap(self.logo)
        frames = [frame.split(',') for frame in data if frame]
        for frame in frames:
            self.update_pixels(frame)
            utime.sleep(0.1)

    def gallery(self):
        """
        Display a gallery of images on the NeoPixel grid.
        """
        images = [
            [0,0,0,0,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,0,27,16,1,27,16,1,20,0,0,0,0,0,11,24,1,0,16,1,33,0,0,33,0,0,11,24,1,0,0,0,33,0,0,33,0,0,20,0,0,0,0,0,0,0,0,0,0,0,3,0,0,3,0,0], # apple
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,0,25,25,0,16,0,0,0,0,0,0,9,19,1,0,12,1,25,0,11,25,0,16,9,19,1,0,0,0,20,0,16,25,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # cherry
            [0,0,0,25,0,0,25,0,0,25,0,0,0,0,0,25,0,0,0,0,0,0,0,0,0,0,0,25,0,0,25,0,0,0,0,0,6,0,0,6,0,0,0,0,0,25,0,0,0,0,0,2,0,0,25,0,0,0,0,0,0,0,0,25,0,0,25,0,0,0,0,0,0,0,0], # debian
        ]
        print("smolPaint: \033[7mGallery mode\033[0m.")
        for img in images:
            self.draw_bitmap(img)
            utime.sleep(1)

# To use this refactored code, you would do something like the following:
# sp = smolPaint()
# sp.gallery()
# while True:
#     data = input(""Paste tokens > ")
#     sp.transfer(data)  # or sp.animator([data]) for multiple frames

sp = smolPaint()
sp.gallery()
while True:
    data = input("Paste tokens > ")
    sp.transfer(data)  # or sp.animator([data]) for multiple frames
