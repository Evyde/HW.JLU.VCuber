import math
import time
from tkinter import Tk
from BasicDraw import BasicDraw
import Coordinates

MAX_X, MAX_Y = 640, 480

window = Tk()
window.title("VCuber - Made By Evyde")

a = BasicDraw(window, MAX_X, MAX_Y)

CUBE_LENGTH = 200

simple_cube = Coordinates.get_vertices(0, 0, 0, CUBE_LENGTH // 2)

print(simple_cube)

r = 0
j = 0

color_list = ['#c7980a', '#f4651f', '#82d8a7', '#cc3a05', '#575e76', '#156943', '#0bd055', '#acd338']


def test_draw():
    global r, j
    r += 0.5
    a.clear()
    a.draw_cube(simple_cube, rot_z=r, rot_x=r, rot_y=r, trans_x=r, trans_y=r, trans_z=r, method="正",
                custom_color=color_list)
    window.after(50, test_draw)


test_draw()
window.mainloop()
