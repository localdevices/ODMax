import numpy as np
import py360convert

# processing functions for ODMax
def reproject_cube(img, **kwargs):
    """
    Reprojects image to a cube projection
    :param img:
    :param face_w: int defining the length of each face of the cube (default: 256)
    :param mode: str defining the reprojection mode, can be 'bilinear' or 'nearest'
    :param kwargs: keyword arguments to pass to py360convert library
    :return: list of ndarrays in shape of [H, W, 3] containing images of cube faces
    """
    assert (isinstance(img, np.ndarray)), "provided img is not a numpy array"
    return py360convert.e2c(img, cube_format="list", **kwargs)
