ODMax
=====

ODMax is a utility to extract still frames from 360-degree videos. At this moment ODMax works with GoPro videos. It may or may not work with other 360 degree camera brands and models but this has not been tested.

To get started with ODMax, set-up a python environment. We recommend using a miniconda or anaconda environment. We have conveniently packaged all dependencies for you, and with `conda` these can be installed easily.

Installation for direct use
---------------------------
If you simply want to add ODMax to an existing python installation or virtual environment, then follow these instructions.

First activate the environment you want ODMax to be installed in (if you don't care about virtual environments, then simply skip this step)

Then install ODMax as follows:
```
pip install git+https://github.com/localdevices/ODMax.git

```
That's it! You are good to go!

Installation from code base
---------------------------

To install ODMax from scratch in a new virtual environment go through these steps:

First, clone the code with `git`

```
git clone https://github.com/localdevices/ODMax.git
```

Setup a virtual environment as follows
```
cd ODMax
conda env create -f environment.yml
```

Now install the ODMax package. If you want to develop ODMax please type
```
pip install -e .
```
If you just want to use ODMax type:
```
pip install .
```
That's it, you are good to go.

Project organisation
--------------------

    .
    ├── README.md
    ├── LICENSE
    ├── setup.py            <- setup script compatible with pip
    ├── environment.yml     <- YML-file for setting up a conda environment with dependencies
    ├── notebooks           <- Jupyter notebooks with examples
    ├── odmax               <- odmax library
        ├── ...             <- odmax functions
    ├── scripts             <- Contains the odmax executable for use on command-line
        ├── odmax           <- Command-line utility for ODMax

