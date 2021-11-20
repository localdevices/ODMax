#!/usr/bin/python3
import sys
import numpy as np
import odmax
from optparse import OptionParser


def main():
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
        print(f"Reprojection mode:   {options.mode}")
        print(f"Face width:          {options.face_w}")
    print(f"======================")
    print(f"Start processing:")
    print(f"======================")
    f = odmax.io.open_file(options.infile)
    # get start and end frame
    start_frame = odmax.io.get_frame_number(f, options.start_time)
    end_frame = odmax.io.get_frame_number(f, options.end_time)
    # TODO: extract metadata
    frame_n = list(range(start_frame, end_frame, options.d_frame))
    for n in frame_n:
        # extract frame
        print("Processing frame {:05d}".format(n))
        img = odmax.io.read_frame(f, n)
        if options.reproject:
            # reproject img to faces
            img = odmax.process.reproject_cube(
                img,
                face_w=options.face_w,
                mode=options.mode
            )
        # TODO: time stamp img
        # write file or files in case of cube
        odmax.io.write_frame(
            img,
            path=options.outpath,
            prefix="{:s}_{:04d}".format(options.prefix, n),
            encoder=options.encoder
        )
    print("")


def create_parser():
    parser = OptionParser()
    parser.add_option(
        "-i",
        "--infile",
        dest="infile",
        nargs=1,
        help='Input video file, compatible with OpenCV2'
    )
    parser.add_option(
        "-o",
        "--outpath",
        dest="outpath",
        nargs=1,
        help='Directory to write output files.',
        default=".",
    )
    parser.add_option(
        "-p",
        "--prefix",
        dest="prefix",
        nargs=1,
        help='Prefix to use for written image files',
        default="still"
    )
    parser.add_option(
        "-c",
        "--encoder",
        dest="encoder",
        nargs=1,
        help='encoder to use to write stills (default: jpg). Can be "jpg", "bmp", "jp2", "png" or "webp"',
        default="jpg"
    )
    parser.add_option(
        "-s",
        "--start-time",
        dest="start_time",
        nargs=1,
        type="float",
        help='Start time in seconds from start of movie',
        default=0.
    )
    parser.add_option(
        "-e",
        "--end-time",
        dest="end_time",
        nargs=1,
        type="float",
        help='End time in seconds from start of movie',
        default=-1.
    )
    parser.add_option(
        "-d",
        "--frame-interval",
        dest="d_frame",
        nargs=1,
        type="int",
        help="Interval between frames (default: 1, integer)",
        default=1,
    )
    parser.add_option(
        "-r",
        "--reproject",
        dest="reproject",
        action="store_true",
        help='Reproject 360 degree stills to cube with 6 faces',
        default=False,
    )
    parser.add_option(
        "-f",
        "--face-width",
        dest="face_w",
        nargs=1,
        type="int",
        help='Length of faces of reprojected cube in pixels (default: 256). Only used in combination with --reproject',
        default=256
    )
    parser.add_option(
        "-m",
        "--mode",
        dest="mode",
        nargs=1,
        help='Mode of reprojection interpolation, can be "bilinear" or "nearest" (default: "nearest"). Only used in combination with --reproject, default: "bilinear"',
        default="bilinear"
    )
    if len(sys.argv[1:]) == 0:
        print("No arguments supplied")
        parser.print_help()
        sys.exit()
    return parser


if __name__ == '__main__':
    main()
