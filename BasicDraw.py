import math
from tkinter import Canvas
import Coordinates


class BasicDraw:
    projection_map_dict = {
        "正": {
            "single": Coordinates.project_3d_to_2d_ortho,
            "multi": Coordinates.project_3d_to_2d_ortho_coordinates
        },
        "斜等轴": {
            "single": Coordinates.project_3d_to_2d_oblique_isometric,
            "multi": Coordinates.project_3d_to_2d_oblique_isometric_coordinates
        },
        "斜二测": {
            "single": Coordinates.project_3d_to_2d_oblique_diametric,
            "multi": Coordinates.project_3d_to_2d_oblique_diametric_coordinates
        }
    }

    def __init__(self, window, width: int, height: int, background_color="#ffffff", axis_x=0, axis_y=0,
                 projection_method="正", canvas=None):
        self.WIDTH = width
        self.HEIGHT = height
        self.axis_x = axis_x
        self.axis_y = axis_y
        self.projection_method = projection_method
        self.axis_length = 0
        if not canvas:
            # Create default canvas
            canvas = Canvas(window, width=width, height=height, bg=background_color)
        canvas.pack()
        self.__panel = canvas

    def clear(self):
        self.__panel.delete("all")

    def get_panel(self):
        return self.__panel

    def update_cached_variables(self):
        pass

    def change_projection_method(self, method: str):
        self.projection_method = method
        self.update_cached_variables()

    def draw_pixel(self, x: int, y: int, color="#000000"):
        # :) Treat 0 square's rectangle as a pixel.
        # It is faster than PhotoImage.put() according to https://gist.github.com/calebmadrigal/81f3b9de14f54ac355f7
        self.__panel.create_oval(self.map_coordinates(x, y), outline=color, width=1)

    def draw_pixels(self, coordinates: tuple[tuple], custom_color=False):
        color = "#000000"
        for coordinate in coordinates:
            if custom_color:
                x, y, color = coordinate
            else:
                x, y = coordinate
            self.draw_pixel(x, y, color)

    def draw_line(self, start_x: int, start_y: int, end_x: int, end_y: int, color="#000000"):
        for coordinate in Coordinates.bresenham(start_x, start_y, end_x, end_y):
            self.draw_pixel(coordinate[0], coordinate[1], color)
        # self.__panel.create_line(
        #     start_x + self.WIDTH // 2, start_y + self.HEIGHT // 2,
        #     end_x + self.WIDTH // 2, end_y + self.HEIGHT // 2,
        #     fill=color, smooth=False, width=1
        # )

    def draw_lines(self, coordinates: tuple[tuple], custom_color=False):
        color = "#000000"
        for coordinate in coordinates:
            if custom_color:
                start_x, start_y, end_x, end_y, color = coordinate
            else:
                start_x, start_y, end_x, end_y = coordinate
            self.draw_line(start_x, start_y, end_x, end_y, color)

    def draw_text(self, x: int, y: int, text="", color="#000000"):
        x, y, _, _ = self.map_coordinates(x, y)
        self.__panel.create_text(x, y, text=text, fill=color)

    def draw_axis(self, axis_length, rot_x=0, rot_y=0, rot_z=0):
        """

        Parameters
        ----------
        rot_x, rot_y, rot_z
            Rotation that you want to display this axis.
        axis_length
            Axis length, like 10 or 30.

        Returns
        -------
        Nothing.
        """
        self.axis_length = axis_length
        origin_coordinate = (0, 0, 0)
        text_tuple = ("X轴", "Y轴", "Z轴")
        origin_color = ("00", "00", "00")
        start_x, start_y = self.axis_x, self.axis_y

        for i in range(3):
            temp_coordinate = list(origin_coordinate)
            temp_color = list(origin_color)
            temp_coordinate[i] = -axis_length
            temp_color[i] = "ff"
            temp_color = "#{}".format("".join(temp_color))
            end_x, end_y, end_z = temp_coordinate
            end_x, end_y = BasicDraw.projection_map_dict[self.projection_method]["single"](end_x, end_y, end_z, rot_x,
                                                                                           rot_y, rot_z)
            self.draw_line(start_x - end_x, start_y - end_y, start_x + end_x, start_y + end_y, color=temp_color)
            self.draw_text(start_x + end_x, start_y + end_y, text=text_tuple[i], color=temp_color)

    def draw_cube_status(self, cubes_status: dict):
        """

        Parameters
        ----------
        cubes_status
            A dict that describe the cubes' status, for example:
            {"Main_Cube": {"color": "#fff0f0", "center_x": 3, "center_y": 3, "center_z": 3}}
            Temporarily fields could use:
                - color: The color of the cube point.
                - trans_x, trans_y, trans_z: The translations along the x, y, and z axes, respectively.
                - center_x, center_y, center_z: The source center axes of this cube.

        Returns
        -------

        """
        for cube_name in cubes_status.keys():
            # Draw oval that represent for cube.
            x, y = \
                BasicDraw.projection_map_dict[self.projection_method]["single"](
                    cubes_status[cube_name]["center_x"],
                    cubes_status[cube_name]["center_y"],
                    cubes_status[cube_name]["center_z"],
                    trans_x=self.map_into_range(cubes_status[cube_name]["trans_x"], -self.WIDTH // 2, self.WIDTH // 2,
                                                -self.axis_length, self.axis_length),
                    trans_y=self.map_into_range(cubes_status[cube_name]["trans_y"], -self.HEIGHT // 2, self.HEIGHT // 2,
                                                -self.axis_length, self.axis_length),
                    trans_z=self.map_into_range(cubes_status[cube_name]["trans_z"],
                                                -(math.sqrt((self.HEIGHT // 2) ** 2 + (self.WIDTH // 2) ** 2)),
                                                math.sqrt((self.HEIGHT // 2) ** 2 + (self.WIDTH // 2) ** 2),
                                                -math.sqrt(self.axis_length ** 2 + self.axis_length ** 2),
                                                math.sqrt(self.axis_length ** 2 + self.axis_length ** 2)),
                    rot_x=cubes_status[cube_name]["rot_x"],
                    rot_y=cubes_status[cube_name]["rot_y"],
                    rot_z=cubes_status[cube_name]["rot_z"]
                )
            # Draw cube name
            self.draw_text(self.axis_x + x, self.axis_y + y, text=cube_name,
                           color=cubes_status[cube_name]["color"])
            # Draw cube point
            # self.__panel.create_oval(self.map_coordinates(self.axis_x + x, self.axis_y + y),
            #                          outline=cubes_status[cube_name]["color"], fill=cubes_status[cube_name]["color"],
            #                          width=5)

    def draw_rectangle(self, coordinates: tuple, custom_color="#000000", fill=False):
        lines = len(coordinates)
        if fill:
            self.polygon_fill(coordinates, custom_color)
        for i in range(lines):
            start_x, start_y = coordinates[i]
            end_x, end_y = coordinates[(i + 1) % lines]
            self.draw_line(start_x, start_y, end_x, end_y, custom_color)
            # self.panel.create_line(start_x, start_y, end_x, end_y, fill=custom_color, width=1, smooth=True)

    def draw_cube(self, coordinates: tuple, rot_x=0, rot_y=0, rot_z=0, trans_x=0, trans_y=0, trans_z=0,
                  custom_color=[]):
        for i in range(6):
            if custom_color:
                color = custom_color[i]
            else:
                color = "#000000"
            self.draw_rectangle(
                BasicDraw.projection_map_dict[self.projection_method]["multi"](coordinates[i], rot_x, rot_y, rot_z,
                                                                               trans_x, trans_y,
                                                                               trans_z), color)

    def polygon_fill(self, polygon, color="#0000ff"):
        # Find this poly's highest point and lowest point
        min_y = int(min(polygon, key=lambda temp_y: temp_y[1])[1])
        max_y = int(max(polygon, key=lambda temp_y: temp_y[1])[1])

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

    @staticmethod
    def map_into_range(original_value, original_min, original_max, new_min, new_max):
        new_value = (original_value - original_min) * (new_max - new_min) / (original_max - original_min) + new_min
        return int(new_value)

    def get_method(self):
        return self.projection_method
