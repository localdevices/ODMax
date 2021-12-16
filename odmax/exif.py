import os
import piexif
from fractions import Fraction
# recipe derived from https://gist.github.com/c060604/8a51f8999be12fc2be498e9ca56adc72
def to_deg(value, loc):
    """
    Convert decimal coordinates into degrees, munutes and seconds tuple

    :param value: coordinate value (float)
    :param loc: direction list, either ["S", "N"] or ["W", "E"]
    :return: tuple like (25, 13, 48.343 ,'N')
    """
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg =  int(abs_value)
    t1 = (abs_value-deg)*60
    min = int(t1)
    sec = round((t1 - min)* 60, 5)
    return (deg, min, sec, loc_value)


def change_to_rational(number):
    """
    Convert a number to rational

    :param number: float (abbreviated to e.g. 1 decimal)
    :return: tuple, (int: numerator, int: denominator)
    """


    """

    Keyword arguments: number
    return: tuple like (1, 2), (numerator, denominator)
    """
    f = Fraction(str(number))
    return (f.numerator, f.denominator)


def set_gps_location(lat, lon, elev):
    """Adds GPS position as EXIF metadata

    Keyword arguments:
    file_name -- image file
    lat -- latitude (as float)
    lon -- longitude (as float)
    elev -- elevation (as float, rounded to 1 decimal)

    """
    lat_deg = to_deg(lat, ["S", "N"])
    lon_deg = to_deg(lon, ["W", "E"])

    exiv_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
    exiv_lon = (change_to_rational(lon_deg[0]), change_to_rational(lon_deg[1]), change_to_rational(lon_deg[2]))
    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSAltitudeRef: 1 if elev < 0 else 0,
        piexif.GPSIFD.GPSAltitude: change_to_rational(round(elev, 1)),
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: exiv_lat,
        piexif.GPSIFD.GPSLongitudeRef: lon_deg[3],
        piexif.GPSIFD.GPSLongitude: exiv_lon,
    }
    return gps_ifd
