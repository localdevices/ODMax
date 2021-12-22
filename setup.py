#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="odmax",
    version="0.1.1",
    description="odmax extracts still images from GoPro 360 camera types, including GNSS location and time information",
    long_description=readme + "\n\n",
    long_description_content_type="text/markdown",
    url="https://github.com/localdevices/ODMax",
    author="Hessel Winsemius and Stephen Mather",
    author_email="info@rainbowsensing.com",
    packages=find_packages(),
    package_dir={"odmax": "odmax"},
    test_suite="tests",
    #use_scm_version=True,
    #setup_requires=["setuptools_scm"],
    python_requires=">=3.8",
    install_requires=[
        "pip",
        "numpy==1.21.4",
        "opencv-python-headless==4.5.4.60",
        "gpxpy==1.5.0",
        "tqdm==4.62.3",
        "piexif==1.1.3",
        "matplotlib==3.5.1",
        "pandas==1.3.5",
        "geopandas==0.10.2",
        "Pillow==8.4.0",
    ],
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
