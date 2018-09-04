from PIL import Image
from DiamondDash.screenshot import Capturer
from DiamondDash.mouse import Mouse
import time
import random


colors = {}
C = Capturer(1048, 341)
M = Mouse(1048, 341)


def get_color(RGB):
    if all(val < 60 for val in RGB):
        return "B"
    elif RGB in colors:
        return colors[RGB]
    else:
        return '?'


def get_fuzzy_color(RGB):
    if all(val < 60 for val in RGB):
        return "B"
    for val, color in colors.items():
        if all(abs(rgb - v) < 10 for rgb, v in zip(RGB, val)):
            return color
    return '?'


class Grid:
    def __init__(self, grid_size_x, grid_size_y, cell_size, img=()):
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.cell_size = cell_size
        if img:
            self.img = img
        else:
            self.take_screenshot()

    def take_screenshot(self):
        self.img = C.grab(0, 0, self.grid_size_x * self.cell_size, self.grid_size_y * self.cell_size)

    def get_cell(self, x, y):
        if x < self.cell_size_x and y < self.grid_size_y:
            return self.img.crop((x * self.cell_size,
                                  y * self.cell_size,
                                  (x + 1) * self.cell_size - 1,
                                  (y + 1) * self.cell_size - 1,
                                  ))
        else:
            return ()

    def get_cell_rgb(self, x, y):
        x0 = x * self.cell_size
        y0 = y * self.cell_size
        return tuple([int(sum(val) / len(val)) for val in zip(
            self.img.getpixel((x0 + 10, y0 + 10)),
            self.img.getpixel((x0 + 10, y0 + 30)),
            self.img.getpixel((x0 + 30, y0 + 30)),
            self.img.getpixel((x0 + 30, y0 + 10)),
            self.img.getpixel((x0 + 20, y0 + 20)),
        )])

    def valid_cell(self, x, y):
        return True
        x0 = x * self.cell_size
        y0 = y * self.cell_size
        return (get_color(self.img.getpixel((x0, y0 + 6))) == "B" \
                and get_color(self.img.getpixel((x0, y0 + 33))) == "B") or \
               (get_color(self.img.getpixel((x0 + 39, y0 + 6))) == "B" \
                and get_color(self.img.getpixel((x0 + 39, y0 + 33))) == "B")

    def get_cell_color(self, x, y):
        """
        print(self.get_cell(x, y).getpixel((0, 6)),
              get_color(self.get_cell(x, y).getpixel((0, 6))),
              self.get_cell(x, y).getpixel((0, 7)),
              get_color(self.get_cell(x, y).getpixel((0, 7))),
              )
        """

        """
        if get_color(self.get_cell(x, y).getpixel((0, 6))) == "B":
            return get_fuzzy_color(self.get_cell(x, y).getpixel((0, 7)))
        else:
            return "?"
        """
        if self.valid_cell(x, y):
            return get_fuzzy_color(self.get_cell_rgb(x, y))
        else:
            return "?"

    def analyse_cell(self, x, y):
        cell = self.get_cell_color(x, y)
        if cell in ["1"]:
            return cell
        if cell == "?" or cell == "B":
            return "."
        cpt = 0
        if x > 0:
            if self.get_cell_color(x - 1, y) == cell:
                cpt += 1
        if x < self.grid_size_x - 1:
            if self.get_cell_color(x + 1, y) == cell:
                cpt += 1
        if cpt > 1:
            return "x"
        if y > 0:
            if self.get_cell_color(x, y - 1) == cell:
                cpt += 1
        if cpt > 1:
            return "x"
        if y < self.grid_size_y - 1:
            if self.get_cell_color(x, y + 1) == cell:
                cpt += 1
        if cpt > 1:
            return "x"
        return "."

    def click_cell(self, x, y):
        M.mouse_pos((x + 0.5) * self.cell_size,
                    (y + 0.5) * self.cell_size)
        M.left_click()
        # print("click on", (x, y))

    def seek_and_destroy(self):
        targets = []
        priority_targets = []
        for y in range(self.grid_size_y):
            for x in range(self.grid_size_x):
                target = self.analyse_cell(x, y)
                if target == "!":
                    self.click_cell(x, y)
                    return
                elif target == "1":
                    priority_targets.append((x,y))
                elif target == "x":
                    targets.append((x, y))
        if priority_targets:
            self.click_cell(*random.choice(priority_targets))
            return
        if targets:
            self.click_cell(*random.choice(targets))


def calibration():
    img = Image.open("reference.png")
    grid = Grid(7, 2, 40, img)
    for y in range(3):
        colors[grid.get_cell_rgb(0, y)] = 'g'
        colors[grid.get_cell_rgb(1, y)] = 'y'
        colors[grid.get_cell_rgb(2, y)] = 'r'
        colors[grid.get_cell_rgb(3, y)] = 'b'
        colors[grid.get_cell_rgb(4, y)] = 'p'
    for x in range(5):
        colors[grid.get_cell_rgb(x, 3)] = '!'
    for x in range(3):
        colors[grid.get_cell_rgb(x, 4)] = '1'


def main():
    grid = Grid(10, 9, 40)
    calibration()

    # grid.get_cell(8,8).show()
    while True:
        """
        for y in range(9):
            line = []
            for x in range(10):
                line.append(grid.get_cell_color(x, y))
            print(" ".join(line))
        """
        """
        print()
        for y in range(9):
            line = []
            for x in range(9):
                line.append(grid.analyse_cell(x, y))
            print(" ".join(line))
        """
        grid.seek_and_destroy()
        time.sleep(0.03)

        grid.take_screenshot()
        # print('-----')


if __name__ == "__main__":
    main()
