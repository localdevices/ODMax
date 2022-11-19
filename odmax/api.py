# here, high-level API classes are defined
import io as IO
import os
import numpy as np
from scipy.interpolate import interp1d
import geopandas as gpd
import pandas as pd
import cv2
import odmax
from datetime import timedelta, datetime
import matplotlib.pyplot as plt

exif_available = odmax.helpers.assert_cli_exe("exiftool")

class Video:
    def __init__(self, fn):
        """
        Create a new Video instance. Properties of the video, relevant for extracting frames will be extracted.
        Also GPS information, if available (tested for GoPro .mp4 format) will be automatically extracted, provided
        that `exiftool` is available on your system and in your system's path. You will receive warnings if `exiftool`
        is not available.

        :param fn: filename of video file on disk
        """
        self.fn = fn
        self.cap = odmax.io.open_file(self.fn)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.start_datetime = None
        self.exif = False
        if exif_available:
            self.exif = True
            self.gpx = odmax.io.get_gpx(self.fn)
            # make lists of lats, lons and timestamps, for use in interpolation
            lat, lon, elev, t = odmax.helpers.parse_coords_from_gpx(self.gpx)
            self.df_gps = pd.DataFrame(
                {
                    "lat": lat,
                    "lon": lon,
                    "elev": elev,
                },
                index=t,
            )
            self.gdf_gps = gpd.GeoDataFrame(
                self.df_gps,
                geometry=gpd.points_from_xy(
                    self.df_gps.lon,
                    self.df_gps.lat,
                    crs=4326,
                )
            )
            try:
                point = odmax.helpers.gpx_find_first_timestamp(self.gpx)
            except:
                print(f"Warning: No GPS information found in file {self.fn}. Skipping GPS parsing.")
                self.exif = False
        # check if we have proper GPS data with time stamps available or not
        if self.exif:
            if point.time is None:
                print(f"Warning: No time information found in GPS track of {fn}. Skipping GPS parsing.")
                # set exif processing to False because we can't parse coordinates without any time info
                self.exif = False
            else:
                print("Found first location and time stamp in video on lat: {}, lon: {}, elev: {}, time: {}".format(
                    point.latitude,
                    point.longitude,
                    point.elevation,
                    point.time.strftime("%Y-%m-%dT%H:%M:%S.%f")[0:-3] + "Z"
                )
                )
                self.start_datetime = point.time

    def get_gps(self, t):
        """
        Returns GPS information at given timestamp t (measured as time epoch, e.g. returned from datetime.timestamp)

        :param t: float from datetime.timestamp (i.e. seconds since 1970-01-01 00:00:00)
        :return: Pandas DataFrame row with location (lat, lon, elev) and index as time epoch, using linear interpolation
        """
        if t <= self.df_gps.index[0]:
            return self.df_gps.drop(columns="geometry").iloc[0]
        if t >= self.df_gps.index[-1]:
            return self.df_gps.drop(columns="geometry").iloc[-1]
        df_select = pd.concat(
            [
                self.df_gps[self.df_gps.index <= t].iloc[-1:],
                pd.DataFrame({k: np.nan for k in self.df_gps.keys()}, index=[t]),
                self.df_gps[self.df_gps.index >= t].iloc[:1],
            ], axis=0
        )
        # interpolate to the missing value
        df_select.drop(columns=["geometry"], inplace=True)
        df_select.interpolate(method="index", inplace=True)
        # return the middle filled value by linear interpolation
        return df_select.iloc[1]

    def get_frame(self, n, reproject=False, **kwargs):
        """
        Get one Frame from Video for processing

        :param n: int, frame number
        :param reproject: bool, set to True if you want to reproject to 6 cube-faces
        :param kwargs: keyword arguments for cube reprojection, see odmax.process.reproject_cube.
        :return: odmax.Frame instance
        """
        # compute timestamp of requested frame
        if self.start_datetime:
            t = self.start_datetime + timedelta(seconds=n/self.fps)
        else:
            t = None
        img = odmax.io.read_frame(self.cap, n)
        if reproject:
            img = odmax.process.reproject_cube(
                img,
                **kwargs
            )
        if self.exif:
            # retrieve coordinate
            coord = self.get_gps(t.timestamp())
            # lat, lon, elev = odmax.helpers.coord_interp(t.timestamp(), timestamps, lats, lons, elevs)
            gps_exif = odmax.exif.set_gps_location(**coord)
            exif_dict = {
                "GPS": gps_exif
            }
        else:
            coord = None
            exif_dict = {}
        return Frame(img, n, t, coord, exif=self.exif, exif_dict=exif_dict)

    def plot_gps(self, geographical=False, figsize=(13, 8), ax=None, crs=None, tiles=None, plot_kwargs={}, zoom_level=8, tiles_kwargs={}):
        """
        Make a simple plot of the gps track in the Video

        :param geographical: bool, use a geographical plot, default False, requires cartopy to be installed
        :param figsize: tuple, passed to plt.figure as figsize
        :param ax: pass an axes that you already have, to add to existing axes
        :param crs: cartopy.crs object, coordinate reference system (default: cartopy.crs.PlateCarree())
        :param tiles: str, name of cartopy.io.img_tiles WMTS WMTS service, default: None, can be e.g. "OSM", "QuadtreeTiles", "GoogleTiles"
        :param zoom_level: int, zoom level for chosen tile service, default 8.
        :param plot_kwargs: dictionary of options to pass to matplotlib.pyplot.plot
        :param tiles_kwargs: dictionary of options to pass to cartopy.axes.add_image
        :return: axes object
        """
        if not(self.exif):
            raise AttributeError("GPS data not available")
        # determine a bbox
        if ax is None:
            f = plt.figure(figsize=figsize)
            if geographical:
                try:
                    import cartopy
                    import cartopy.io.img_tiles as cimgt
                    import cartopy.crs as ccrs
                    from shapely.geometry import LineString
                except:
                    raise ModuleNotFoundError('Geographic plotting requires cartopy. Please install it with "conda install cartopy" and try again')
                bbox = list(np.array(LineString(self.gdf_gps.geometry.values).bounds)[[0, 2, 1, 3]])
                if crs is None:
                    crs = ccrs.PlateCarree()
                ax = plt.subplot(projection=crs)
                ax.set_extent(bbox, crs=ccrs.PlateCarree())
                if tiles is not None:
                    tiler = getattr(cimgt, tiles)()
                    ax.add_image(tiler, zoom_level, **tiles_kwargs)
                self.gdf_gps.plot(ax=ax, transform=ccrs.PlateCarree(), zorder=2, **plot_kwargs)
            else:
                ax = f.add_subplot()
                self.gdf_gps.plot(ax=ax, zorder=2, **plot_kwargs)
        else:
            self.gdf_gps.plot(ax=ax, zorder=2, **plot_kwargs)

        return ax


class Frame:
    def __init__(self, img, n, t, coord, exif=False, exif_dict={}):
        """
        Create a new Frame instance. A Frame holds the image, but also which frame number it came from, the coordinate
        of the frame if GPS information is available, and the EXIF tag that belongs to the frame, comprised of a dictionary

        :param img: ND-array [M, N, 3] holding the RGB image
        :param n: frame number
        :param t: timestamp as datetime.datetime object
        :param coord: pandas DataFrame row holding latitude, longitude, elevation and time
        :param exif_dict: dict, holding EXIF tag information, e.g. exif_dict["GPS"] should contain a dict with GPS tags
        """
        self.frame_number = n
        self.timestamp = t
        self.coord = coord
        self.exif_dict = exif_dict
        self.img = img

    def to_file(self, path=".", prefix="still", encoder="jpg"):
        """
        Write a frame to one or multiple files. If cube-face reprojection has been used
        6 images will be written at the selected path and prefix. Names of files will follow
        the following conventions:
        In case no reprojection used: <path>/<prefix>_<frame_number>.<encoder>
        In case cube-face reprojection is applied: <path>/<prefix>_<frame_number>_<cube face>.<encoder>

        where cube_face is one of "F", "R", "B", "L", "U", "D" as suffixes for
        "front", "right", "back", "left", "up" and "down".

        :param path: str, Path to write frames to
        :param prefix: str, Prefix for files
        :param encoder: str, default is "jpg"
        :return: str, output filename; or list of str filenames
        """
        if isinstance(self.img, list):
            # a 6-face cube is provided, write 6 individual images
            assert (len(self.img) == 6), f"6 images are expected with cube reprojection, but {len(self.img)} were found"
            fns = []
            for i, c in zip(self.img, odmax.consts.CUBE_SUFFIX):
                assert ((len(i.shape) == 3) and (i.shape[
                                                     -1] >= 3)), "One of the images you provided is incorrectly shaped, must be 3 dimensional with the last dimension as RGB"
                fn = os.path.join(path, "{:s}_{:04d}_{:s}.{:s}".format(prefix, self.frame_number, c, encoder.lower()))
                # write file in PIL
                odmax.io.write_frame(i, fn, encoder=encoder, exif_dict=self.exif_dict)
                fns.append(fn)
            return fns
        else:
            # a single image is provided
            fn = os.path.join(path, "{:s}_{:04d}.{:s}").format(prefix, self.frame_number, encoder.lower())
            odmax.io.write_frame(self.img, fn, encoder=encoder, exif_dict=self.exif_dict)
            return fn

    def to_bytes(self, encoder="jpg"):
        """
        Write a frame to one or more bytestreams, ready to push to an online service.
        If cube-face reprojection has been used 6 images will be written in a list of bytestreams

        :param encoder: str, default is "jpg"
        :return: bytestream
        """
        if isinstance(self.img, list):
            # a 6-face cube is provided, write 6 individual images
            assert (len(self.img) == 6), f"6 images are expected with cube reprojection, but {len(self.img)} were found"
            bytes = []
            for i, c in zip(self.img, odmax.consts.CUBE_SUFFIX):
                assert ((len(i.shape) == 3) and (i.shape[
                                                     -1] >= 3)), "One of the images you provided is incorrectly shaped, must be 3 dimensional with the last dimension as RGB"
                buffer = IO.BytesIO()
                # write file in PIL
                odmax.io.write_frame(i, buffer, encoder=encoder, exif_dict=self.exif_dict)
                # to_pil(i).save(fn_out, p_encoder.lower(), exif=exif)
                buffer.seek(0)
                bytes.append(buffer.read())
            return bytes
        else:
            buffer = IO.BytesIO()
            odmax.io.write_frame(self.img, buffer, encoder=encoder, exif_dict=self.exif_dict)
            buffer.seek(0)
            return buffer.read()

    def plot(self, figsize=(8, 8), rows=2, cols=3):
        """

        :param figsize: tuple (height, width) of figure, default: (8, 8)
        :param rows: int, number of rows to use for plotting 6 cube-faces, default: 2
        :param cols: int, number of cols to use for plotting 6 cube-faces, default: 3
        :return: f, ax, figure and axes handle
        """
        # make a simple plot, and make it dependent on this
        f = plt.figure(figsize=figsize)
        if self.coord is not None:
            coordstr = "Location: lat: {:3.7f}, lon: {:3.7f}, elev: {:5.2f}".format(self.coord.lat, self.coord.lon, self.coord.elev)
        else:
            coordstr = "Location: unknown"
        if self.timestamp is not None:
            timestr = "Time: " + self.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[0:-3] + "Z"
        else:
            timestr = "Time: unknown"
        if isinstance(self.img, list):
            # a 6-face cube is provided, write 6 individual images
            assert (len(self.img) == 6), f"6 images are expected with cube reprojection, but {len(self.img)} were found"
            for n, (i, c) in enumerate(zip(self.img, odmax.consts.CUBE_SUFFIX)):
                ax = plt.subplot(rows, cols, n + 1)
                ax.imshow(i)
                ax.set_title(c)
                ax.tick_params(
                    left=False,
                    right=False,
                    labelleft=False,
                    labelbottom=False,
                    bottom=False,
                )
        else:
            ax = plt.axes()
            ax.imshow(self.img)
            ax.tick_params(
                left=False,
                right=False,
                labelleft=False,
                labelbottom=False,
                bottom=False,
            )
        f.suptitle(f"{timestr} \n {coordstr}")
        return f, ax
