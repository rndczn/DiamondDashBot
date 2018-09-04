import win32api, win32con
import time


class Mouse:
    def __init__(self, x_pad, y_pad):
        self.x_pad = x_pad
        self.y_pad = y_pad

    def mouse_pos(self, x, y):
        win32api.SetCursorPos((int(self.x_pad + x), int(self.y_pad + y)))

    def left_click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        #time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def get_cords(self):
        x, y = win32api.GetCursorPos()
        x = x - self.x_pad
        y = y - self.y_pad
        return x, y


if __name__ == "__main__":
    m = Mouse(1048, 341)
    for _ in range(30):
        print(m.get_cords())
        time.sleep(1)
