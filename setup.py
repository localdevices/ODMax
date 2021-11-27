#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="odmax",
    description="odmax extracts still images from GoPro 360 camera types, including GNSS location and time information",
    long_description=readme + "\n\n",
    url="https://github.com/localdevices/ODMax",
    author="Hessel Winsemius and Stephen Mather",
    author_email="info@rainbowsensing.com",
    packages=find_packages(),
    package_dir={"odmax": "odmax"},
    test_suite="tests",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    python_requires=">=3.8",
    install_requires=[
        "pip",
        "numpy",
        "opencv-python-headless",
        "PyExifTool",
        "py360convert @ git+https://github.com/localdevices/py360convert.git",
        # "py360convert==0.1.0"

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
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Photogrammetry",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="GoPro, OpenDroneMap",
)
