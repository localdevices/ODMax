# I/O functionality for ODMax
import os
import cv2
from odmax import consts, helpers
from datetime import datetime
import gpxpy
from PIL import Image

# high level variables
PATH = os.path.dirname(__file__)
gpx_fmt_fn = os.path.join(PATH, "gpx.fmt")
if os.name == "posix":
    null_output = "/dev/null 2>&1"
else:
    null_output = "nul"

# pil uses specific encoder names such as "jpeg", translate if necessary using the below dict
pil_encoders = {
    "jpg": "jpeg"
}

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

def write_frame(img, path=".", prefix="still", encoder="jpg", exif="".encode()):
    """
    Writes a frame to a file. If a 6-face cube list is provided, 6 files will be written using
    "F", "R", "B", "L", "U", "D" as suffixes for "front", "right", "back", "left", "up" and "down".

    :param img: ndarray or list of 6 ndarrays of size [H, W, 3]
    :param path: path to write frame to
    :param prefix: prefix of file to write to
    :param exif: byte-formatted encoder info to pass as exif tags
    :return:
    """
    def to_pil(array):
        """
        Converts ND-array into PIL object

        :param array: ND-array with colors (3rd dimension) in RGB order
        :return: PIL image
        """
        return Image.fromarray(cv2.cvtColor(array, cv2.COLOR_BGR2RGB))


    if isinstance(img, list):
        # a 6-face cube is provided, write 6 individual images
        assert (len(img)==6), f"6 images are expected with cube reprojection, but {len(img)} were found"
        fns = []
        for i, c in zip(img, consts.CUBE_SUFFIX):
            assert ((len(i.shape) == 3) and (i.shape[-1] >= 3)), "One of the images you provided is incorrectly shaped, must be 3 dimensional with the last dimension as RGB"
            fn_out = os.path.join(path, "{:s}_{:s}.{:s}".format(prefix, c, encoder.lower()))
            # write file in PIL
            if encoder in pil_encoders:
                # translate
                p_encoder = pil_encoders[encoder]
            else:
                p_encoder = encoder
            to_pil(i).save(fn_out, p_encoder.lower(), exif=exif)
            # cv2.imwrite(fn_out, i)
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


