import base64
import tempfile
from tkinter import Tk, Menu
from BasicDraw import BasicDraw
import Coordinates

MAX_X, MAX_Y = 640, 480
AXIS_LENGTH = 50
CUBE_LENGTH = 150
ROTATION_STEP = 1
TRANSLATION_STEP = 5
COLOR_LIST = ['#c7980a', '#f4651f', '#82d8a7', '#cc3a05', '#575e76', '#156943', '#0bd055', '#acd338']

rotation_x = 0
rotation_y = 0
rotation_z = 0
translation_x = 0
translation_y = 0
translation_z = 0
frame = 0
fps = 0
introduction = True


def do_popup(event):
    # Display the popup menu
    try:
        popup.tk_popup(event.x_root, event.y_root, False)
    finally:
        popup.grab_release()


def do_translation(event):
    global rotation_x, rotation_y, rotation_z, translation_x, translation_y, translation_z
    match event.char:
        case 'a':
            translation_x -= TRANSLATION_STEP
            if translation_x <= -MAX_X // 2:
                translation_x = -MAX_X // 2
        case 'd':
            translation_x += TRANSLATION_STEP
            if translation_x >= MAX_X // 2:
                translation_x = MAX_X // 2


def fps_timer():
    global frame, fps
    fps = frame
    frame = 0
    window.after(1000, fps_timer)


def update():
    global rotation_x, rotation_y, rotation_z, frame, translation_x, translation_y, translation_z, fps
    frame += 1
    draw.clear()
    draw.draw_axis(AXIS_LENGTH, rotation_x, rotation_x, rotation_x)
    draw.draw_cube(simple_cube, rot_z=rotation_z, rot_x=rotation_x, rot_y=rotation_y, method="正",
                   custom_color=COLOR_LIST, trans_x=translation_x, trans_y=translation_y, trans_z=translation_z)
    draw.draw_cube_status(
        {
            "方块儿": {
                "color": COLOR_LIST[0], "center_x": 0, "center_y": 0, "center_z": 0,
                "trans_x": translation_x, "trans_y": translation_y, "trans_z": translation_z,
                "rot_z": rotation_z, "rot_x": rotation_x, "rot_y": rotation_y
            }
        }
    )
    draw.draw_text(-MAX_X // 2 + 50, -MAX_Y // 2 + 10, "FPS: {}".format(fps), "#000000")
    if introduction:
        draw.draw_text(MAX_X // 2 - 100, -MAX_Y // 2 + 10, "WSADQE: x, y, z轴平移")
    window.after(1, update)


def toggle_introduction():
    global introduction
    introduction = not introduction


if __name__ == "__main__":
    window = Tk()
    window.title("VCuber - Made By Evyde")
    window.resizable(False, False)

    # Create ICON
    with tempfile.TemporaryDirectory() as tmp_dir:
        import icon

        with open(tmp_dir + "/icon.ico", "wb") as tmp:
            tmp.write(base64.b64decode(icon.img))
            window.iconbitmap(tmp_dir + "/icon.ico")

    draw = BasicDraw(window, MAX_X, MAX_Y, axis_x=-MAX_X // 2 + 2 * AXIS_LENGTH, axis_y=-MAX_Y // 2 + 2 * AXIS_LENGTH)
    simple_cube = Coordinates.get_vertices(0, 0, 0, CUBE_LENGTH // 2)

    # Create popup menu
    popup = Menu(window, tearoff=False)
    projection = Menu(popup, tearoff=False)
    projection.add_command(label="正投影", command=lambda: draw.change_projection_method("正"))
    projection.add_command(label="斜二测投影", command=lambda: draw.change_projection_method("斜二测"))
    projection.add_command(label="斜等轴投影", command=lambda: draw.change_projection_method("斜等轴"))
    popup.add_cascade(label="投影切换", menu=projection)
    # popup.add_command(label="重置", command=reset)
    popup.add_command(label="开/关使用说明", command=toggle_introduction)
    popup.add_separator()
    popup.add_command(label="退出", command=window.destroy)

    # Bind event
    window.bind("<Button-2>", do_popup)
    window.bind("<Key>", do_translation)

    # Draw and loop
    update()
    fps_timer()
    window.mainloop()
