import shutil
from subprocess import Popen, PIPE, call, run
import numpy as np

def assert_cli_exe(cmd):
    """
    Assert if a command-line OS command is available

    :param cmd: str, command to check
    :return: True if command exists, false if not
    """
    return shutil.which(cmd) is not None

def exiftool(*args):
    process = Popen(['exiftool'] + list(args), stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        print(f"WARNING: exceptions found during processing: {stderr.decode()}")
    return stdout.decode()

def gpx_find_first_timestamp(gpx):
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # lat, lon, elev, time = point.latitude, point.longitude, point.elevation, point.time
                if point.time is not None:
                    break
    return point

def parse_coords_from_gpx(gpx, remove_missing=True):
    """
    Converts gpx object into lists of lats, lons and timestamps (since epoch 1970-01-01 00:00:00)

    :param gpx: GPX object (parsed from gpxpy)
    :return: lats, lons, timestamps, np.ndarray vectors
    """
    # extract lats/lons for each point
    times = [p.time for t in gpx.tracks for s in t.segments for p in s.points]
    lons = np.array([p.longitude for t in gpx.tracks for s in t.segments for p in s.points]).astype("float")
    lats = np.array([p.latitude for t in gpx.tracks for s in t.segments for p in s.points]).astype("float")
    elevs = np.array([p.elevation for t in gpx.tracks for s in t.segments for p in s.points]).astype("float")
    timestamps = np.array([t.timestamp() if t is not None else np.nan for t in times]).astype("float")
    if remove_missing:
        # remove places with NaN in timestamps from lists
        lons = lons[np.isfinite(timestamps)]
        lats = lats[np.isfinite(timestamps)]
        elevs = elevs[np.isfinite(timestamps)]
        timestamps = timestamps[np.isfinite(timestamps)]
    return lats, lons, elevs, timestamps


def coord_interp(t, ts, lats, lons, elevs):
    """
    Interpolate latitude / longitude coordinate from a timestamp

    :param t:
    :param ts:
    :param lats:
    :param lons:
    :param elevs:
    :return:
    """
    lat = np.interp(t, ts, lats)
    lon = np.interp(t, ts, lons)
    elev = np.interp(t, ts, elevs)
    return lat, lon, elev
