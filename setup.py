#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages
from pkg_resources import DistributionNotFound, get_distribution

#https://stackoverflow.com/a/49338206
def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None

install_deps = [
        "pip",
        "numpy",
        "gpxpy",
        "tqdm",
        "piexif",
        "matplotlib",
        "pandas",
        "geopandas==0.10.2",
        "Pillow",
    ]

# If any opencv package is available we can use it
# as installing multiple opencv packages breaks things
if (get_dist('opencv-contrib-python-headless') is None
and get_dist('opencv-python-headless') is None
and get_dist('opencv-contrib-python') is None
and get_dist('opencv-python') is None):
    install_deps.append('opencv-python-headless')

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="odmax",
    version="0.1.2",
    description="odmax extracts still images from GoPro 360 camera types, including GNSS location and time information",
    long_description=readme + "\n\n",
    long_description_content_type="text/markdown",
    url="https://github.com/localdevices/ODMax",
    author="Hessel Winsemius and Stephen Mather",
    author_email="info@rainbowsensing.com",
    packages=find_packages(),
    package_dir={"odmax": "odmax"},
    test_suite="tests",
    python_requires=">=3.8",
    install_requires=install_deps,
    extras_require={
        "dev": ["pytest", "pytest-cov"],
        "optional": [],
    },
    entry_points={
        "console_scripts": [
            "odmax=odmax.cli:main"
        ]
    },
    include_package_data=True,
    license="AGPLv3",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="GoPro, OpenDroneMap",
)
