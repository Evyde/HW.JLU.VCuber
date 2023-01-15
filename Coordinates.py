import math

import numpy as np


def normalize_3d(position):
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)


def normalize_2d(position):
    x, y = position
    x, y = (int(round(x)), int(round(y)))
    return (x, y)


def bresenham(start_x, start_y, end_x, end_y):
    coordinates = []
    # Use Bresenham to draw a line
    if start_x == end_x and start_y == end_y:
        coordinates.append((start_x, start_y))
        return coordinates
    dx = abs(end_x - start_x)
    dy = abs(end_y - start_y)
    x, y = start_x, start_y
    sx = -1 if start_x > end_x else 1
    sy = -1 if start_y > end_y else 1

    if dx > dy:
        err = dx / 2.0
        while x != end_x:
            coordinates.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != end_y:
            coordinates.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    return coordinates


def basic_trans(rot_x, rot_y, rot_z, trans_x, trans_y, trans_z, x, y, z):
    rot_x = np.deg2rad(rot_x)
    rot_y = np.deg2rad(rot_y)
    rot_z = np.deg2rad(rot_z)

    rot_matrix_x = np.array([[1, 0, 0],
                             [0, np.cos(rot_x), -np.sin(rot_x)],
                             [0, np.sin(rot_x), np.cos(rot_x)]])
    rot_matrix_y = np.array([[np.cos(rot_y), 0, np.sin(rot_y)],
                             [0, 1, 0],
                             [-np.sin(rot_y), 0, np.cos(rot_y)]])
    rot_matrix_z = np.array([[np.cos(rot_z), -np.sin(rot_z), 0],
                             [np.sin(rot_z), np.cos(rot_z), 0],
                             [0, 0, 1]])
    rot_matrix = rot_matrix_x @ rot_matrix_y @ rot_matrix_z
    coords = np.array([x, y, z])
    coords += np.array([trans_x, trans_y, trans_z])
    coords = rot_matrix @ coords

    return coords


def project_3d_to_2d_oblique_diametric(x, y, z, rot_x=0, rot_y=0, rot_z=0, trans_x=0, trans_y=0, trans_z=0):
    """Project 3D coordinates to 2D coordinates using an oblique diametric projection.

    Parameters
    ----------
    x, y, z : float
        The 3D coordinates to be projected.
    rot_x, rot_y, rot_z : float, optional
        The angles of rotation around the x, y, and z axes, respectively. Default is 0 for all.
    trans_x, trans_y, trans_z : float, optional
        The translations along the x, y, and z axes, respectively. Default is 0 for all.

    Returns
    -------
    tuple of float
        The projected 2D coordinates.
    """
    # Apply rotations and translations
    coords_rotated = basic_trans(rot_x, rot_y, rot_z, trans_x, trans_y, trans_z, x, y, z)
    # Project to 2D using an oblique diagonal projection
    x, y, z = coords_rotated
    return normalize_2d((x + 0.354 * y, -0.354 * y + z))


def project_3d_to_2d_oblique_diametric_coordinates(coordinates: tuple[tuple], rot_x=0, rot_y=0, rot_z=0, trans_x=0,
                                                   trans_y=0, trans_z=0):
    temp_list = []
    for i in coordinates:
        x, y, z = i
        temp_list.append(project_3d_to_2d_oblique_diametric(x, y, z, rot_x, rot_y, rot_z, trans_x, trans_y, trans_z))
    return tuple(temp_list)


def project_3d_to_2d_oblique_isometric(x, y, z, rot_x=0, rot_y=0, rot_z=0, trans_x=0, trans_y=0, trans_z=0):
    """Project 3D coordinates to 2D coordinates using an oblique isometric projection.

    Parameters
    ----------
    x, y, z : float
        The 3D coordinates to be projected.
    rot_x, rot_y, rot_z : float, optional
        The angles of rotation around the x, y, and z axes, respectively. Default is 0 for all.
    trans_x, trans_y, trans_z : float, optional
        The translations along the x, y, and z axes, respectively. Default is 0 for all.

    Returns
    -------
    tuple of float
        The projected 2D coordinates.
    """
    # Apply rotations and translations
    x, y, z = basic_trans(rot_x, rot_y, rot_z, trans_x, trans_y, trans_z, x, y, z)
    # Project to 2D using an oblique isometric projection

    return normalize_2d((x - 0.707 * y, +0.707 * y + z))


def project_3d_to_2d_oblique_isometric_coordinates(coordinates: tuple[tuple], rot_x=0, rot_y=0, rot_z=0, trans_x=0,
                                                   trans_y=0, trans_z=0):
    temp_list = []
    for i in coordinates:
        x, y, z = i
        temp_list.append(project_3d_to_2d_oblique_isometric(x, y, z, rot_x, rot_y, rot_z, trans_x, trans_y, trans_z))
    return tuple(temp_list)


def project_3d_to_2d_ortho(x, y, z, rot_x=0, rot_y=0, rot_z=0, trans_x=0, trans_y=0, trans_z=0):
    """Project 3D coordinates to 2D coordinates using an orthographic projection.

    Parameters
    ----------
    x, y, z : float
        The 3D coordinates to be projected.
    rot_x, rot_y, rot_z : float, optional
        The angles of rotation around the x, y, and z axes, respectively. Default is 0 for all.
    trans_x, trans_y, trans_z : float, optional
        The translations along the x, y, and z axes, respectively. Default is 0 for all.

    Returns
    -------
    tuple of float
        The projected 2D coordinates.
    """
    # Apply rotations and translations
    coords = basic_trans(rot_x, rot_y, rot_z, trans_x, trans_y, trans_z, x, y, z)

    # Project to 2D using an orthographic projection
    return normalize_2d((coords[0], coords[1]))


def project_3d_to_2d_ortho_coordinates(coordinates: tuple[tuple], rot_x=0, rot_y=0, rot_z=0, trans_x=0, trans_y=0,
                                       trans_z=0):
    temp_list = []
    for i in coordinates:
        x, y, z = i
        temp_list.append(project_3d_to_2d_ortho(x, y, z, rot_x, rot_y, rot_z, trans_x, trans_y, trans_z))
    return tuple(temp_list)


def get_vertices(x, y, z, n):
    """Returns the vertices of a cube with center (x, y, z) and side length 2n."""
    return ([
        ((x - n, y + n, z - n), (x - n, y + n, z + n), (x + n, y + n, z + n), (x + n, y + n, z - n)),  # top
        ((x - n, y - n, z - n), (x + n, y - n, z - n), (x + n, y - n, z + n), (x - n, y - n, z + n)),  # bottom
        ((x - n, y - n, z - n), (x - n, y - n, z + n), (x - n, y + n, z + n), (x - n, y + n, z - n)),  # left
        ((x + n, y - n, z + n), (x + n, y - n, z - n), (x + n, y + n, z - n), (x + n, y + n, z + n)),  # right
        ((x - n, y - n, z + n), (x + n, y - n, z + n), (x + n, y + n, z + n), (x - n, y + n, z + n)),  # front
        ((x + n, y - n, z - n), (x - n, y - n, z - n), (x - n, y + n, z - n), (x + n, y + n, z - n)),  # back
    ])
