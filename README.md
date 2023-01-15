# VCuber

[![VCuber | Compile](https://github.com/Evyde/VCuber/actions/workflows/VCuberCompile.yml/badge.svg?branch=master)](https://github.com/Evyde/VCuber/actions/workflows/VCuberCompile.yml)

This is a homework from JLU's computer graphics lesson.

## Function

- [X] Draw a cube using Bresenham to draw a line.
- [X] Switch through the menu to display the orthographic and oblique isometric projections of the cube.
- [X] Use keyboard to control the panning of this cube.
- [X] Use mouse to control the rotation of this cube.

## Library Usage

This is a library called `BasicDraw`, which is made by me and has some userful tools build from scratch like drawing a pixel and a line.

To initialize this tool, you need to have `Tk` imported, and create a window. For example,

```python
from tkinter import Tk
from BasicDraw import BasicDraw


window = Tk()
panel = BasicDraw(window, 1920, 1080)

panel.draw_pixel(0, 1, color="#f0f0f0")
panel.draw_pixels(((0, 1, "#f0f0f0"), ), custom_color=True)
panel.draw_pixels(((0, 1), ), custom_color=False)

panel.draw_line(0, 0, 100, 100, color="#f0f0f0", enable_warning=True)
panel.draw_lines(((0, 0, 1, 1, "#f0f0f0"), ), custom_color=True)
panel.draw_lines(((0, 0, 1, 1), ), custom_color=False)

panel.clear()

panel.draw_rectangle(((0, 0), (0, 4), (4, 4), (4, 0)), custom_color="#f0f0f0")
panel.polygon_fill(((0, 0), (0, 4), (4, 4), (4, 0)), color="#f0f0f0")
# Pass verticals of 6 faces
panel.draw_cube(((0, 0, 0), (), (), (), (), ()), rot_x=0, rot_y=0, rot_z=0, method="正")
```

The init method of `BasicDraw` takes 4 arguments, which are:

- The tk object.
- Width of the panel.
- Height of the panel.
- Color of the background (Default is "#ffffff").

You can see other method's usage above. 

When finish drawing, do not forget to call the `tkinter.mainloop()` to maintain the window.

## Notice

Since performance issues, I've changed my custom draw method from bresenham to tkinter's `create_line`
when I ensure my bresenham works properly. When using my method, it is 5 FPS in PC, 60 FPS in M1 macOS,
which is unbearable. If you want to experience the origin version, please edit the `draw_line` method in `BasicDraw`,
comment line 66-70 and uncomment line 64-65.
