from tkinter import Tk
from BasicDraw import BasicDraw

MAX_X, MAX_Y = 640, 480

window = Tk()
window.title("VCuber - Made By Evyde")

a = BasicDraw(window, MAX_X, MAX_Y)



a.draw_line(-50, -50, 50, 50)
a.draw_line(50, -50, -50, 50)
a.draw_line(50, 50, -50, 50)
a.draw_line(50, 50, 50, -50)
a.draw_line(-50, -50, -50, 50)
a.draw_line(-50, -50, 50, -50)

a.polygon_fill([(-49, -49), (49, -49), (49, 49), (-49, 49)], "#37b336")

window.mainloop()