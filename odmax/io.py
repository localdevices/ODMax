# I/O functionality for ODMax
import os.path
import cv2
from datetime import datetime

def read_frame(f, n):
    """
    Reads frame number n from opened video file f
    :param f: pointer to opened video file
    :param n: frame number
    :return: img, blob containing frame
    """
    # TODO: assert of f
    assert(n, int), f"{n} is not an integer"
    # FIXME: complete this code
    raise NotImplementedError("Not implemented yet")
    return img



def to_file(fn, img, driver=None):
    """
    Write image to a file with provided driver name
    :param fn: filename to write to
    :param img: blob containing still image
    :param driver: driver to use for writing, can be "tif", "png", "jpg"
    :return: None
    """
    if not(os.path.isdir(os.path.split(fn)[0])):
        raise IOError(f"Path {os.path.split(fn)[0]} is not available")

    # TODO: check if the driver is valid
    # FIXME: complete this code
    raise NotImplementedError("Not implemented yet")


def get_exif(fn, fn_out):
    """
    Reads the exif tag from a video and writes it to a file
    :param fn: video filename
    :param fn_out: text file to write exif tag to
    :return:
    """
    if not(os.path.isfile(fn)):
        raise IOError(f"File {fn} does not exist")
    if not(os.path.isdir(os.path.split(fn_out)[0])):
        raise IOError(f"Path {os.path.split(fn_out)[0]} is not available")
    # FIXME: complete this code
    raise NotImplementedError("Not implemented yet")


def get_gpx(fn, fn_out):
    """
    Reads the gpx track from a video and writes it to a file
    :param fn: video filename
    :param fn_out: text file to write exif tag to
    :return:
    """
    if not(os.path.isfile(fn)):
        raise IOError(f"File {fn} does not exist")
    if not(os.path.isdir(os.path.split(fn_out)[0])):
        raise IOError(f"Path {os.path.split(fn_out)[0]} is not available")
    # TODO: return if GPX info is not found

    # FIXME: complete this code
    raise NotImplementedError("Not implemented yet")


def timestamp(fn, t):
    """
    time stamps an existing file containing a still image
    :param fn: existing file with still image
    :param t: datetime object, to write to still image's exif tag
    :return:
    """
    if not(os.path.isfile(fn)):
        raise IOError(f"File {fn} does not exist")
    assert(isinstance(t, datetime)), f"{t} is not a datetime object"
    # FIXME: complete this code
    raise NotImplementedError("Not implemented yet")
