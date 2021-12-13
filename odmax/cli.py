#!/usr/bin/python3
import os.path
import sys
import cv2
import numpy as np
import odmax
import piexif
from odmax.helpers import assert_cli_exe
from optparse import OptionParser
from datetime import datetime, timedelta
from tqdm import tqdm

def main():
    """
    odmax can be called from command-line. Please type `odmax` without input arguments or `odmax --help` for command-line
    arguments

    :return:
    """
    parser = create_parser()
    (options, args) = parser.parse_args()
    # assertions below
    if not(options.infile):
        raise IOError("No input file provided, please use -i option to provide a valid video file")
    if options.end_time < 0:
        options.end_time = np.inf
    if options.end_time <= options.start_time:
        raise ValueError(f"End time {options.end_time} is smaller or equal than start time {options.start_time}")
    if options.d_frame < 1:
        raise ValueError(f"Frame difference {options.d_frame} is smaller than one, has to be at least one")
    exif = assert_cli_exe("exiftool")
    # do something
    print(f"Processing video  : {options.infile}")
    print(f"Output path       : {options.outpath}")
    print(f"Encoder           : {options.encoder.lower()}")
    print(f"File prefix       : {options.prefix}")
    print(f"Start time        : {options.start_time} seconds")
    print(f"End time          : {options.end_time} seconds")
    print(f"Frame interval    : {options.d_frame}")
    print(f"Reprojection      : {'enabled' if options.reproject else 'disabled'}")
    if options.reproject:
        print(f"Reprojection mode : {options.mode}")
        print(f"Face width        : {options.face_w if options.face_w is not None else 'not set, estimated from video'}")
    if not(os.path.isdir(options.outpath)):
        print(f"Output path {options.outpath} does not exist, creating path...")
        os.makedirs(options.outpath)
    if exif:
        print(f"exiftool          : found! Processing with GPS coordinates if available")
        # import exiftool
    else:
        print(f"exiftool          : NOT found. Processing WITHOUT GPS coordinates. Install exiftool if you wish to process with coordinates.")

    print(f"====================")
    print(f"Start processing:")
    print(f"====================")
    print(f"Collecting metadata:")
    print(f"--------------------")

    f = odmax.io.open_file(options.infile)
    # get start and end frame
    start_frame = odmax.io.get_frame_number(f, options.start_time)
    end_frame = odmax.io.get_frame_number(f, options.end_time)
    fps = f.get(cv2.CAP_PROP_FPS)
    print(f"Processing from frame {start_frame} until frame {end_frame} on FPS {fps}")
    if exif:
        gpx = odmax.io.get_gpx(options.infile)
        # make lists of lats, lons and timestamps, for use in interpolation
        lats, lons, elevs, timestamps = odmax.helpers.parse_coords_from_gpx(gpx)
        print(elevs)

        # write to file
        fn_gpx = os.path.join(options.outpath, "track.gpx")
        xml = gpx.to_xml()
        with open(fn_gpx, "w") as txt:
            txt.write(xml)
        try:
            point = odmax.helpers.gpx_find_first_timestamp(gpx)
        except:
            print(f"Warning: No GPS information found in file {options.infile}. Skipping GPS parsing.")
            exif = False
    if exif:
        if point.time is None:
            print(f"Warning: No time information found in GPS track of {options.infile}. Skipping GPS parsing.")
            # set exif processing to False because we can't parse coordinates without any time info
            exif = False
        else:
            print("Found first time stamp on lat: {}, lon: {}, elev: {}, time: {}".format(
                point.latitude,
                point.longitude,
                point.elevation,
                point.time.strftime("%Y-%m-%dT%H:%M:%S.%f")[0:-3] + "Z"
            )
            )
            start_datetime = point.time
    print(f"-----------------------")
    print(f"Running for all frames:")
    print(f"-----------------------")

    frame_n = list(range(start_frame, end_frame, options.d_frame))
    # compute seconds from start
    frame_t = [frame/fps for frame in frame_n]
    # compute datetimes
    if exif:
        # prepare all info for exiftool time stamping
        frame_datetime = [start_datetime + timedelta(seconds=t) for t in frame_t]
    else:
        frame_datetime = frame_t
    work = tqdm(range(len(frame_n)))
    #
    # work = tqdm(zip(frame_n, frame_datetime))
    import time
    for i in work:
        n = frame_n[i]
        t = frame_datetime[i]
        work.set_description("Processing frame {:5d}".format(n))
        img = odmax.io.read_frame(f, n)
        if options.reproject:
            # reproject img to faces
            img = odmax.process.reproject_cube(
                img,
                face_w=options.face_w,
                mode=options.mode,
                overlap=options.overlap
            )
        if exif:
            # retrieve coordinate
            print(t.timestamp())
            lat, lon, elev = odmax.helpers.coord_interp(t.timestamp(), timestamps, lats, lons, elevs)

            print(lat, lon, elev)
            gps_exif = odmax.exif.set_gps_location(lat, lon, elev)
            exif_dict = {
                "GPS": gps_exif
            }
            # if not(isinstance(fn_imgs, list)):
            #     fn_imgs = [fn_imgs]
            # for fn_img in fn_imgs:
            #     # time stamp image(s)
            #     odmax.io.timestamp(fn_img, t)
            #     res = odmax.io.geostamp(fn_img, fn_gpx)
            # if res != 0:
            #     work.set_description(f"Warning: {fn_img} could not be GPS stamped properly.")
        else:
            exif_dict = {}

        fn_imgs = odmax.io.write_frame(
            img,
            path=options.outpath,
            prefix="{:s}_{:04d}".format(options.prefix, n),
            encoder=options.encoder,
            exif=piexif.dump(exif_dict)
        )

def create_parser():
    parser = OptionParser()
    parser.add_option(
        "-i",
        "--infile",
        dest="infile",
        nargs=1,
        help='Input video file, compatible with OpenCV2. Place path between " " to ensure spaces are interpreted correctly.'
    )
    parser.add_option(
        "-o",
        "--outpath",
        dest="outpath",
        nargs=1,
        help='Directory to write output files (default: "."). Place path between " " to ensure spaces are interpreted correctly.',
        default=".",
    )
    parser.add_option(
        "-p",
        "--prefix",
        dest="prefix",
        nargs=1,
        help='Prefix to use for written image files (default: "still").',
        default="still"
    )
    parser.add_option(
        "-c",
        "--encoder",
        dest="encoder",
        nargs=1,
        help='encoder to use to write stills (default: jpg). Can be "jpg", "bmp", "jp2", "png" or "webp".',
        default="jpg"
    )
    parser.add_option(
        "-s",
        "--start-time",
        dest="start_time",
        nargs=1,
        type="float",
        help='Start time in seconds from start of movie (default: 0.0).',
        default=0.
    )
    parser.add_option(
        "-e",
        "--end-time",
        dest="end_time",
        nargs=1,
        type="float",
        help='End time in seconds from start of movie (default: end of movie).',
        default=-1.
    )
    parser.add_option(
        "-d",
        "--frame-interval",
        dest="d_frame",
        nargs=1,
        type="int",
        help="Frame step size (default: 1, integer). 1 means all frames between start and end time are processed, 2 means every second frame is processed, etc.",
        default=1,
    )
    parser.add_option(
        "-r",
        "--reproject",
        dest="reproject",
        action="store_true",
        help='Reproject 360 degree stills to cube with 6 faces (default: not set, i.e. no reprojection is performed).',
        default=False,
    )
    parser.add_option(
        "-f",
        "--face-width",
        dest="face_w",
        nargs=1,
        type="int",
        help='Length of faces of reprojected cube in pixels (default: not set, the optimal resolution will be estimated from the video file). Only used in combination with --reproject.',
    )
    parser.add_option(
        "-m",
        "--mode",
        dest="mode",
        nargs=1,
        help='Mode of reprojection interpolation, can be "bilinear" or "nearest" (default: "bilinear"). Only used in combination with --reproject.',
        default="bilinear"
    )
    parser.add_option(
        "--overlap",
        dest="overlap",
        nargs=1,
        type="float",
        help='Overlap in cube faces in ratio of face length without overlap. (default: 0.1). This setting ensures that each face shares part of its objective with its neighbouring faces. Only used in combination with --reproject.',
        default=0.1
    )
    if len(sys.argv[1:]) == 0:
        print("No arguments supplied")
        parser.print_help()
        sys.exit()
    return parser


if __name__ == '__main__':
    main()
    parser = create_parser()
