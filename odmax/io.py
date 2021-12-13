# I/O functionality for ODMax
import os.path
import cv2
from odmax import consts, helpers
from datetime import datetime
import gpxpy

PATH = os.path.dirname(__file__)
gpx_fmt_fn = os.path.join(PATH, "gpx.fmt")

def open_file(fn):
    """
    Open file for reading by cv2.

    :param fn: video file (cv2 compatible)
    :return: cv2 pointer to file
    """
    assert(isinstance(fn, str)), "No valid file provided, should be of type str"
    assert(os.path.isfile(fn)), f"File {fn} was not found"
    if isinstance(fn, str):
        # try to open file with openCV
        f = cv2.VideoCapture(fn)
        if not(f.isOpened()):
            raise(f"Could not recognise file {fn} as a proper video file")
        return f
    else:
        raise TypeError(f"{fn} should be a string pointing to a path")

def get_frame_number(f, time):
    """
    Get the frame number belonging to the defined time in seconds.

    :param f: pointer to opened video file
    :param time: seconds from start of video
    :return:
    """
    fps = f.get(cv2.CAP_PROP_FPS)
    frame_count = f.get(cv2.CAP_PROP_FRAME_COUNT)
    return int(min(frame_count, time * fps))

def read_frame(f, n):
    """
    Reads frame number n from opened video file f.

    :param f: pointer to opened video file
    :param n: frame number
    :return: img, blob containing frame
    """
    assert isinstance(f, cv2.VideoCapture)
    assert isinstance(n, int), f"{n} is not an integer"
    # check if frame is beyond length of movie
    if n > f.get(cv2.CAP_PROP_FRAME_COUNT):
        raise ValueError(f"The requested frame number {n} is larger than the available frames {cv2.CAP_PROP_FRAME_COUNT}")
    # wind to the right frame number
    f.set(cv2.CAP_PROP_POS_FRAMES, n)
    # extract this frame
    success, img = f.read()
    if success:
        return img
    else:
        raise IOError(f"The requested frame {n} could not be extracted. Perhaps the videofile is damaged.")

def write_frame(img, path=".", prefix="still", encoder="jpg"):
    """
    Writes a frame to a file. If a 6-face cube list is provided, 6 files will be written using
    "F", "R", "B", "L", "U", "D" as suffixes for "front", "right", "back", "left", "up" and "down".

    :param img: ndarray or list of 6 ndarrays of size [H, W, 3]
    :param path: path to write frame to
    :param prefix: prefix of file to write to
    :return:
    """
    if isinstance(img, list):
        # a 6-face cube is provided, write 6 individual images
        assert (len(img)==6), f"6 images are expected with cube reprojection, but {len(img)} were found"
        fns = []
        for i, c in zip(img, consts.CUBE_SUFFIX):
            assert ((len(i.shape) == 3) and (i.shape[-1] >= 3)), "One of the images you provided is incorrectly shaped, must be 3 dimensional with the last dimension as RGB"
            fn_out = os.path.join(path, "{:s}_{:s}.{:s}".format(prefix, c, encoder.lower()))
            cv2.imwrite(fn_out, i)
            fns.append(fn_out)
        return fns
    else:
        # a single image is provided
        fn_out = os.path.join(path, "{:s}.{:s}").format(prefix, encoder.lower())
        cv2.imwrite(fn_out, img)
        return fn_out

def get_exif(fn, fn_out):
    """
    Reads the exif tag from a video and writes it to a file.

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


def get_gpx(fn):
    """
    Reads the gpx track from a video and writes it to a file.

    :param fn: video filename
    :return: parsed gpx data
    """
    if not(os.path.isfile(fn)):
        raise IOError(f"File {fn} does not exist")
    return gpxpy.parse(helpers.exiftool('-ee', '-p', f"{gpx_fmt_fn}", fn))


def timestamp(fn, t):
    """
    time stamps an existing file containing a still image.

    :param fn: existing file with still image
    :param t: datetime object, to write to still image's exif tag
    :return:
    """
    assert(isinstance(t, datetime)), f"{t} is not a datetime object"
    if not (os.path.isfile(fn)):
        raise IOError(f"File {fn} does not exist")
    datetimestr = t.strftime("%Y-%m-%d %H:%M:%SZ")
    subsectimestr = t.strftime("%f")[0:-3]
    subsecdatetimestr = t.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"
    # perform exif actions
    cmd = f'exiftool -DateTimeOriginal="{datetimestr}" -SubSecTimeOriginal="{subsectimestr}" -SubSecDateTimeOriginal="{subsecdatetimestr}" -overwrite_original {fn} >/dev/null 2>&1'
    os.system(cmd)

def geostamp(fn_img, fn_gpx):
    if not (os.path.isfile(fn_img)):
        raise IOError(f"File {fn_img} does not exist")
    if not (os.path.isfile(fn_gpx)):
        raise IOError(f"File {fn_gpx} does not exist")
    exif_args = (
        "-Geotag".encode(),
        fn_gpx.encode(),
        '"-Geotime<SubSecDateTimeOriginal"'.encode(),
        fn_img.encode()
    )
    cmd = f'exiftool -Geotag {fn_gpx} "-Geotime<SubSecDateTimeOriginal" -overwrite_original {fn_img} >/dev/null 2>&1'
    res = os.system(cmd)
    return res