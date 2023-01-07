from tkinter import Tk
from math import sin

from BasicDraw import BasicDraw

WIDTH, HEIGHT = 640, 480

window = Tk()
window.title("VCuber - Made By Evyde")

a = BasicDraw(window, WIDTH, HEIGHT)

for x in range(4 * WIDTH):
    y = int(HEIGHT/2 + HEIGHT/4 * sin(x/80.0))
    a.draw_pixel(x // 4, y)

window.mainloop()