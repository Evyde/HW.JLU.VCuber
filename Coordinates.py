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
    return coordinates[0], coordinates[1]


def get_vertices(x, y, z, n):
    """Returns the vertices of a cube with center (x, y, z) and side length 2n."""
    vertices = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            for k in [-1, 1]:
                vertices.append((x + i*n, y + j*n, z + k*n))
    return vertices


def get_faces(vertices):
    """Returns the faces of a cube given a list of its vertices."""
    faces = []
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            if vertices[i][0] == vertices[j][0] and vertices[i][1] == vertices[j][1]:
                # x and y coordinates are the same, so the vertices are on the same face
                face = [vertices[i], vertices[j]]
                for k in range(len(vertices)):
                    if vertices[k][0] == vertices[i][0] and vertices[k][1] == vertices[i][1] and vertices[k] not in face:
                        face.append(vertices[k])
                faces.append(face)
            elif vertices[i][0] == vertices[j][0] and vertices[i][2] == vertices[j][2]:
                # x and z coordinates are the same, so the vertices are on the same face
                face = [vertices[i], vertices[j]]
                for k in range(len(vertices)):
                    if vertices[k][0] == vertices[i][0] and vertices[k][2] == vertices[i][2] and vertices[k] not in face:
                        face.append(vertices[k])
                faces.append(face)
            elif vertices[i][1] == vertices[j][1] and vertices[i][2] == vertices[j][2]:
                # y and z coordinates are the same, so the vertices are on the same face
                face = [vertices[i], vertices[j]]
                for k in range(len(vertices)):
                    if vertices[k][1] == vertices[i][1] and vertices[k][2] == vertices[i][2] and vertices[k] not in face:
                        face.append(vertices[k])
                faces.append(face)
    return faces
