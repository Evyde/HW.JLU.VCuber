# VCuber

This is a homework from JLU's computer graphics lesson.

## Function

- [ ] Draw a cube using Bresenham to draw a line.
- [ ] Switch through the menu to display the orthographic and oblique isometric projections of the cube.
- [ ] Use keyboard to control the panning of this cube.
- [ ] Use mouse to control the rotation of this cube.

## Library Usage

This is a library called `BasicDraw`, which is made by me and has some userful tools build from scratch like drawing a pixel and a line.

To initialize this tool, you need to have `Tk` imported, and create a window. For example,
```python
from tkinter import Tk
from BasicDraw import BasicDraw


window = Tk()
panel = BasicDraw(window, 1920, 1080)
```

The init method of `BasicDraw` takes 4 arguments, which are:

- The tk object.
- Width of the panel.
- Height of the panel.
- Color of the background (Default is "#ffffff").

When finish drawing, do not forget to call the `tkinter.mainloop()` to maintain the window.
