def normalize_3d(position):
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)


def normalize_2d(position):
    x, y = position
    x, y = (int(round(x)), int(round(y)))
    return (x, y)


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
    import numpy as np
    # Apply rotations and translations
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
    coordinates = np.array([x, y, z])
    coordinates = rot_matrix @ coordinates
    coordinates += np.array([trans_x, trans_y, trans_z])

    # Project to 2D using an orthographic projection
    return normalize_2d((coordinates[0], coordinates[1]))


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