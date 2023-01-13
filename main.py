import math
import threading
import time
from tkinter import Tk
from BasicDraw import BasicDraw
import Coordinates

MAX_X, MAX_Y = 640, 480

window = Tk()
window.title("VCuber - Made By Evyde")

a = BasicDraw(window, MAX_X, MAX_Y)

CUBE_LENGTH = 150

simple_cube = Coordinates.get_vertices(0, 0, 0, CUBE_LENGTH // 2)

print(simple_cube)

r = 0
frame = 0

color_list = ['#c7980a', '#f4651f', '#82d8a7', '#cc3a05', '#575e76', '#156943', '#0bd055', '#acd338']


def test_draw():
    global r, frame
    r += 0.5
    r = r % 360
    frame += 1
    a.clear()
    a.draw_cube(simple_cube, rot_z=r, rot_x=r, rot_y=r, method="正",
                custom_color=color_list)
    window.after(1, test_draw)


def fps_timer():
    global frame
    print("FPS: {}".format(frame))
    frame = 0
    window.after(1000, fps_timer)


test_draw()
fps_timer()
window.mainloop()
