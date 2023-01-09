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

r = 0.8
def test():
    global r
    r += math.pi / 180
    a.clear()
    a.draw_cube(simple_cube, rot_z=r, rot_x=r)

    window.after(100, test)


# a.polygon_fill([(-49, -49), (49, -49), (49, 49), (-49, 49)], "#37b336")
test_list = [((-41, 72), (-41, 167), (135, 83), (135, -11)),
((-135, -83), (41, -167), (41, -72), (-135, 11)),
((-135, -83), (-135, 11), (-41, 167), (-41, 72)),
((41, -72), (41, -167), (135, -11), (135, 83)),
((-135, 11), (41, -72), (135, 83), (-41, 167)),
((41, -167), (-135, -83), (-41, 72), (135, -11))]
for i in range(6):
    color = ['#c7980a', '#f4651f', '#82d8a7', '#cc3a05', '#575e76', '#156943', '#0bd055', '#acd338']
    # a.draw_rectangle(test_list[i], color[i])
    print(color[i])
test()
window.mainloop()