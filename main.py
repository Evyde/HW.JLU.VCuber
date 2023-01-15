import base64
import itertools
import math
import threading
import random
from tkinter import Tk, PhotoImage
from BasicDraw import BasicDraw
import Coordinates

MAX_X, MAX_Y = 640, 480
AXIS_LENGTH = 50

window = Tk()
window.title("VCuber - Made By Evyde")

with open("icon.ico", "wb") as tmp:
    import icon
    tmp.write(base64.b64decode(icon.img))

window.iconbitmap("./icon.ico")

a = BasicDraw(window, MAX_X, MAX_Y, axis_x=-MAX_X // 2 + 2 * AXIS_LENGTH, axis_y=-MAX_Y // 2 + 2 * AXIS_LENGTH)

CUBE_LENGTH = 150

simple_cube = Coordinates.get_vertices(0, 0, 0, CUBE_LENGTH // 2)

r = 0
frame = 0
t = 0

color_list = ['#c7980a', '#f4651f', '#82d8a7', '#cc3a05', '#575e76', '#156943', '#0bd055', '#acd338']


def test_draw():
    global r, frame, t
    r += 0.5
    if r % 360 == 0:
        a.change_projection_method(random.choice(list(BasicDraw.projection_map_dict.keys())))
    r = r % 360
    frame += 1
    a.clear()
    a.draw_axis(AXIS_LENGTH, r, r, r)
    a.draw_cube(simple_cube, rot_z=r, rot_x=r, rot_y=r, method="正",
                custom_color=color_list, trans_x=t, trans_y=0, trans_z=0)
    a.draw_cube_status({"方块儿": {"color": "#000000", "center_x": 0, "center_y": 0, "center_z": 0,
                                 "trans_x": t, "trans_y": 0, "trans_z": 0, "rot_z": r, "rot_x": r, "rot_y": r}})
    window.after(1, test_draw)


def fps_timer():
    global frame, t
    print("FPS: {}".format(frame))
    frame = 0
    t -= 10
    window.after(1000, fps_timer)


test_draw()
fps_timer()
window.mainloop()
