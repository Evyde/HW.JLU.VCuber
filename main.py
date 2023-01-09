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

r = 0.635
j = 0
def test():
    global r, j
    if j % 5 == 0:
        r += math.pi / 1800
    j += 1
    a.clear()
    a.draw_cube(simple_cube, rot_z=r, rot_x=r, rot_y=r, trans_x=r, trans_y=r, trans_z=r)

    window.after(1, test)


# a.polygon_fill([(-49, -49), (49, -49), (49, 49), (-49, 49)], "#37b336")
test_list = [((-140, 76), (-140, -46), (19, 51), (19, 172)),
((-19, -51), (140, 46), (140, -76), (-19, -172)),
((-19, -51), (-19, -172), (-140, -46), (-140, 76)),
((140, -76), (140, 46), (19, 172), (19, 51)),
((-19, -172), (140, -76), (19, 51), (-140, -46)),
((140, 46), (-19, -51), (-140, 76), (19, 172))]
for i in range(6):
    color = ['#c7980a', '#f4651f', '#82d8a7', '#cc3a05', '#575e76', '#156943', '#0bd055', '#acd338']
    # a.draw_rectangle(test_list[i], color[i])
    print(color[i])
test()
window.mainloop()