import numpy as np
import py360convert

# processing functions for ODMax
def reproject_cube(img, **kwargs):
    """
    Reprojects image to a cube projection
    :param img: ndarray with dimensions [H, W, 3] containing image
    :param face_w: int defining the length of each face of the cube (default: 256)
    :param mode: str defining the reprojection mode, can be 'bilinear' or 'nearest'
    :param overlap: float, defining the amount of overlap on face edges defined as ratio of face_w (e.g. 0.1). If not set, this will default to 0.1
    :return: list of ndarrays in shape of [H, W, 3] containing images of cube faces
    """
    assert (isinstance(img, np.ndarray)), "provided img is not a numpy array"
    if not "overlap" in kwargs:
        kwargs["overlap"] = 0.1  # always default to 0.1
    if not("face_w" in kwargs):
        # if kwargs["face_w"] is None:
        face_w_no_overlap = int(img.shape[1]/4)  # a quarter of the width of the still
        face_w = int(face_w_no_overlap * (1 + 2 * kwargs["overlap"]))  # add twice the overlap to the face width
        kwargs["face_w"] = face_w
    faces = py360convert.e2c(img, cube_format="list", **kwargs)
    # rearrange coordinates of faces to ensure we look from the inside to the faces
    faces[1] = np.fliplr(faces[1])  # right face is mirrored left-right
    faces[2] = np.fliplr(faces[2])  # back face is mirrored left-right
    faces[4] = np.flipud(faces[4])  # up face is mirrored up-down
    return faces
