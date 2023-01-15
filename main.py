import base64
import math
import tempfile
import time
import tkinter
from tkinter import Tk, Menu
from BasicDraw import BasicDraw
import Coordinates

MAX_X, MAX_Y = 640, 480
AXIS_LENGTH = 50
CUBE_LENGTH = 150
ROTATION_STEP = 5
TRANSLATION_STEP = 5
RETARD_TIME = 2000
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
last_x_angle = 0
last_y_angle = 0
x_speed = 0
y_speed = 0
ctrl = False
axis = True
retard_lock = False
last_time = time.perf_counter() * 1000


def do_popup(event):
    # Display the popup menu
    try:
        popup.tk_popup(event.x_root, event.y_root, False)
    finally:
        popup.grab_release()


def do_translation(event):
    global rotation_x, rotation_y, rotation_z, translation_x, translation_y, translation_z, ctrl
    match event.char:
        case 'w':
            translation_x -= TRANSLATION_STEP
            return
        case 's':
            translation_x += TRANSLATION_STEP
            return
        case 'a':
            translation_y -= TRANSLATION_STEP
            return
        case 'd':
            translation_y += TRANSLATION_STEP
            return
        case 'q':
            translation_z -= TRANSLATION_STEP
            return
        case 'e':
            translation_z += TRANSLATION_STEP
            return
        case 'z':
            rotation_z -= ROTATION_STEP
            return
        case 'x':
            rotation_z += ROTATION_STEP
            return


def do_ctrl(ctrl_status):
    global ctrl
    ctrl = ctrl_status


def do_rotation(event):
    global rotation_x, rotation_y, last_x_angle, last_y_angle, x_speed, y_speed, retard_lock, last_time
    retard_lock = True
    if ctrl:
        rotation_y += event.x_root / MAX_X * 360 % 360 - rotation_y
    else:
        rotation_x += event.y_root / MAX_Y * 360 % 360 - rotation_x
    temp_time = time.perf_counter() * 1000
    div_time = temp_time - last_time
    last_time = temp_time
    x_speed = -(last_x_angle - rotation_x) / div_time
    y_speed = -(last_y_angle - rotation_y) / div_time
    last_x_angle = rotation_x
    last_y_angle = rotation_y


def start_retard(event):
    global retard_lock
    retard_lock = False
    do_retard(0)


def do_retard(now_tick):
    global rotation_x, rotation_y, x_speed, y_speed, retard_lock
    if retard_lock or now_tick >= RETARD_TIME:
        return
    rotation_x += x_speed
    rotation_y += y_speed
    x_speed += get_now_speed(x_speed, RETARD_TIME, now_tick)
    y_speed += get_now_speed(y_speed, RETARD_TIME, now_tick)
    window.after(1, lambda: do_retard(now_tick + 1))


def get_now_speed(initial_velocity, total_time, now_time):
    acceleration = -initial_velocity / total_time
    return acceleration * now_time


def fps_timer():
    global frame, fps
    fps = frame
    frame = 0
    window.after(1000, fps_timer)


def update():
    global rotation_x, rotation_y, rotation_z, frame, translation_x, translation_y, translation_z, fps, axis
    frame += 1
    draw.clear()
    draw.draw_cube(simple_cube, rot_z=rotation_z, rot_x=rotation_x, rot_y=rotation_y,
                   custom_color=COLOR_LIST, trans_x=translation_x, trans_y=translation_y, trans_z=translation_z)
    if axis:
        draw.draw_axis(AXIS_LENGTH, rotation_x, rotation_y, rotation_z)
        draw.draw_cube_status(
            {
                "🤣": {
                    "color": COLOR_LIST[0], "center_x": 0, "center_y": 0, "center_z": 0,
                    "trans_x": translation_x, "trans_y": translation_y, "trans_z": translation_z,
                    "rot_z": rotation_z, "rot_x": rotation_x, "rot_y": rotation_y
                }
            }
        )
    draw.draw_text(-MAX_X // 2 + 50, -MAX_Y // 2 + 10, "FPS: {}".format(fps), "#000000")
    if introduction:
        draw.draw_text(MAX_X // 2 - 120, -MAX_Y // 2 + 60,
                       "鼠标拖动: 绕X, Y轴旋转\nCtrl+鼠标拖动: 切换单独绕X, Y轴旋转\nWSADQE: X, Y, Z轴平移\nZX: 绕Z轴旋转\n鼠标右键: 呼出菜单\n当前: {}投影".format(
                           draw.get_method()))
    window.after(1, update)


def toggle_introduction():
    global introduction
    introduction = not introduction


def toggle_axis_cube_status():
    global axis
    axis = not axis


def reset():
    global rotation_x, rotation_y, rotation_z, translation_x, translation_y, translation_z
    rotation_x = 0
    rotation_y = 0
    rotation_z = 0
    translation_x = 0
    translation_y = 0
    translation_z = 0
    draw.change_projection_method("正")


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
    popup.add_command(label="重置", command=reset)
    popup.add_separator()
    popup.add_command(label="开/关使用说明", command=toggle_introduction)
    popup.add_command(label="开/关坐标轴和方块位置显示", command=toggle_axis_cube_status)
    popup.add_separator()
    popup.add_command(label="退出", command=window.destroy)

    # Bind event
    window.bind("<Button-2>", do_popup)
    window.bind("<Button-3>", do_popup)
    window.bind("<Key>", do_translation)
    window.bind("<B1-Motion>", do_rotation)
    window.bind("<KeyPress-Control_L>", lambda _: do_ctrl(True))
    window.bind("<KeyRelease-Control_L>", lambda _: do_ctrl(False))
    window.bind("<ButtonRelease-1>", start_retard)

    # Draw and loop
    update()
    fps_timer()
    window.mainloop()
