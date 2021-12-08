ODMax
=====

**ODMax** is a utility to extract still frames from 360-degree videos. At this moment **ODMax** works with GoPro videos. It may or may not work with other 360 degree camera brands and models but this has not been tested.

To get started with **ODMax**, set-up a python environment. We recommend using a Miniconda or Anaconda environment. We have conveniently packaged all dependencies for you, and with `conda` these can be installed easily.

> **_note:_**  For instructions how to get Anaconda (with lots of pre-installed libraries) or Miniconda (light weight) installed, please go to https://docs.conda.io/projects/conda/en/latest/

> **_manual:_** A full manual with examples can be found on https://odmax.readthedocs.io/

Installation
------------

### Installation for direct use

If you simply want to add **ODMax** to an existing python installation or virtual environment, then follow these instructions.

First activate the environment you want **ODMax** to be installed in (if you don't care about virtual environments, then simply skip this step)

Then install **ODMax** as follows:
```
pip install odmax
```
That's it! You are good to go!

### Installation from code base

To install **ODMax** from scratch in a new virtual environment for having the latest code changes or for development,
go through these steps:

First, clone the code with `git`

```
git clone https://github.com/localdevices/ODMax.git
```

If you want, setup a virtual environment as follows:
```
cd ODMax
conda env create -f environment.yml
```

Now install the **ODMax** package. If you want to develop **ODMax** please type
```
pip install -e .
```
If you just want to use **ODMax** (without the option to develop on the code) type:
```
pip install .
```
That's it, you are good to go.

### Installation of exiftool for metadata extraction

Especially for photogrammetry or 360 streetview applications, it is essential to have time stamps and geographical
coordinates embedded in the extracted stills. ODMax automatically extracts such information from 360-video files if
these are recorded by the device used. In order to do this, ODMax requires ``exiftool`` to be installed and available on
the path. To install ``exiftool`` in Windows, please follow the download and installation instructions for Windows on
https://exiftool.org/install.html. For Linux, you can also follow the download and installation instructions, or simply
acquire a stable version from the package manager of your installed distribution. 

Using ODMax
-----------
To use **ODMax**, go to a command line and type 
```
odmax --help
```
This will provide an overview of the most up-to-date command line options.
Alternatively, use our jupyter notebook examples to see common use cases on command-line as
well as directly in the API.

Acknowledgement
---------------
The development of ODMax has been funded by the Australian National University - Research School of Biology.

Project organisation
--------------------

    .
    ├── README.md
    ├── LICENSE
    ├── setup.py            <- setup script compatible with pip
    ├── environment.yml     <- YML-file for setting up a conda environment with dependencies
    ├── docs                <- Sphinx documentation source code
        ├── ...             <- Sphinx source code files
    ├── examples            <- Small example files used in notebooks
        ├── ...             <- individual .jpg and .mp4 files
    ├── notebooks           <- Jupyter notebooks with examples how to use the API
        ├── ...             <- individual Jupyter notebooks
    ├── odmax               <- odmax library and CLI
        ├── ...             <- odmax functions and CLI main function .py files

