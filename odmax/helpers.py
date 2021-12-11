import shutil
from subprocess import Popen, PIPE

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
                print(point.latitude)
                print(point.latitude)
                print(point.time)
                # lat, lon, elev, time = point.latitude, point.longitude, point.elevation, point.time
                print('Point at ({0},{1}) -> {2}, time: {3}'.format(point.latitude, point.longitude, point.elevation, point.time))
                if point.time is not None:
                    break
    return point

