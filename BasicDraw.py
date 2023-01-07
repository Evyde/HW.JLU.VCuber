from collections import defaultdict
from tkinter import Canvas


class BasicDraw:
    def __init__(self, window, width: int, height: int, background_color="#ffffff"):
        self.WIDTH = width
        self.HEIGHT = height
        canvas = Canvas(window, width=width, height=height, bg=background_color)
        canvas.pack()
        self.panel = canvas

    def draw_pixel(self, x: int, y: int, color="#000000"):
        # :) Treat 0 square's rectangle as a pixel.
        # It is faster than PhotoImage.put() according to https://gist.github.com/calebmadrigal/81f3b9de14f54ac355f7
        self.panel.create_rectangle(self.map_coordinates(x, y), outline=color)

    def draw_pixels(self, coordinates: list[tuple], custom_color=False):
        color = "#000000"
        for coordinate in coordinates:
            if custom_color:
                x, y, color = coordinate
            else:
                x, y = coordinate
            self.draw_pixel(x, y, color)

    def draw_line(self, start_x: int, start_y: int, end_x: int, end_y: int, color="#000000"):
        # Use Bresenham to draw a line
        if start_x == end_x and start_y == end_y:
            self.draw_pixel(start_x, start_y, color)
            print("DO NOT TRY TO USE DRAW_LINE TO DRAW A PIXEL, USE DRAW_PIXEL INSTEAD!")
            return
        x = start_x
        y = start_y
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        step_x = 1 if end_x > start_x else 0 if end_x == start_x else -1
        step_y = 1 if end_y > start_y else 0 if end_y == start_y else -1
        p = 2 * dy - dx

        while (x <= (end_x if end_x > start_x else start_x)) and (
                x >= (end_x if end_x < start_x else start_x)) and (
                y <= (end_y if end_y > start_y else start_y)) and (
                y >= (end_y if end_y < start_y else start_y)):
            self.draw_pixel(x, y, color)
            if p >= 0:
                y += step_y
                p += 2 * (dy - dx)
            else:
                p += 2 * dy
            x += step_x

    def draw_lines(self, coordinates: list[tuple], custom_color=False):
        color = "#000000"
        for coordinate in coordinates:
            if custom_color:
                start_x, start_y, end_x, end_y, color = coordinate
            else:
                start_x, start_y, end_x, end_y = coordinate
            self.draw_line(start_x, start_y, end_x, end_y, color)

    def draw_cube(self, vertices):
        pass

    def polygon_fill(self, polygon, color="#0000ff"):
        # Find this poly's highest point and lowest point
        min_y = int(min(polygon, key=lambda x: x[1])[1])
        max_y = int(max(polygon, key=lambda x: x[1])[1])

        for y in range(min_y, max_y + 1):
            # Find edge point in this line
            intersections = []
            for i in range(len(polygon)):
                p1 = polygon[i]
                p2 = polygon[(i + 1) % len(polygon)]
                if p1[1] == p2[1]:
                    continue
                if p1[1] > p2[1]:
                    p1, p2 = p2, p1
                if p1[1] <= y < p2[1]:
                    x = p1[0] + (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1])
                    intersections.append(x)
            # Fill!
            intersections.sort()
            for i in range(0, len(intersections), 2):
                for x in range(int(intersections[i]), int(intersections[i + 1]) + 1):
                    self.draw_pixel(x, y, color)

    def map_coordinates(self, x, y):
        x += self.WIDTH // 2
        y += self.HEIGHT // 2
        return (x, y) * 2
