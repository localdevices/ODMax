import numpy as np
import py360convert

# processing functions for ODMax
def reproject_cube(img, **kwargs):
    """
    Reprojects image to a cube projection
    :param img: ndarray with dimensions [H, W, 3] containing image
    :param face_w: int defining the length of each face of the cube (default: 256)
    :param mode: str defining the reprojection mode, can be 'bilinear' or 'nearest'
    :param kwargs: keyword arguments to pass to py360convert library
    :return: list of ndarrays in shape of [H, W, 3] containing images of cube faces
    """
    assert (isinstance(img, np.ndarray)), "provided img is not a numpy array"
    if "face_w" in kwargs:
        if kwargs["face_w"] is None:
            face_w = int(img.shape[1]/4)  # a quarter of the width of the still
            kwargs["face_w"] = face_w
    return py360convert.e2c(img, cube_format="list", **kwargs)
