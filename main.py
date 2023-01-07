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
def test():
    global r
    r += 1
    print(Coordinates.get_faces(simple_cube))
    lines = []
    for i in Coordinates.get_faces(simple_cube):
        temp_line = []
        for j in i:
            x, y, z = j
            for t in Coordinates.project_3d_to_2d_ortho(x, y, z, rot_z=r):
                temp_line.append(t)
        lines.append(tuple(temp_line))

    print(lines)

    a.draw_lines(lines)
    window.after(100, test)


# a.polygon_fill([(-49, -49), (49, -49), (49, 49), (-49, 49)], "#37b336")
test()
window.mainloop()