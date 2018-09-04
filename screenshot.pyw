from PIL import ImageGrab
import os
import time


class Capturer:
    def __init__(self, x_pad, y_pad):
        self.x_pad = x_pad
        self.y_pad = y_pad

    def grabAll(self):
        return ImageGrab.grab()

    def grab(self, x0, y0, x1, y1):
        box = (self.x_pad + x0, self.y_pad + y0, self.x_pad + x1, self.y_pad + y1)
        return ImageGrab.grab(box)


def main():
    c = Capturer(1048, 341)
    im = c.grab(0, 0, 400, 360)
    im.save(os.getcwd() + '\\snap__' + str(int(time.time())) +
            '.png', 'PNG')
    # grabAll()


if __name__ == '__main__':
    main()
