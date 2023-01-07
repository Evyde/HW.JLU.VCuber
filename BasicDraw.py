from tkinter import Canvas


class BasicDraw:
    def __init__(self, window, width: int, height: int, background_color="#ffffff"):
        canvas = Canvas(window, width=width, height=height, bg=background_color)
        canvas.pack()
        self.panel = canvas

    def draw_pixel(self, x: int, y: int, color="#000000"):
        self.panel.create_rectangle(self.map_coordinates(x, y), outline=color)

    def map_coordinates(self, x, y):
        return (x, y) * 2
