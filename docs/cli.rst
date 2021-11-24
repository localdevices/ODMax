.. _cli:

================
Command line use
================
ODMax is first and foremost intended to be a command line utility. You simply call it with


.. code-block:: console

    $ odmax

and with a set of command line arguments. Below the possible arguments are described in full.

.. program-output:: odmax --help

The command line options can also be shown by:

.. code-block:: console

    $ odmax --help

Below we show an example command, assuming you have a video file called `a_walk_in_the_park.mp4` in the folder `/home/random_user/videos`, that you wish to
extract still frames every 25 frames, starting at 10 seconds into the video, and ending at 2 minutes (i.e. 120 seconds).
We also assume that you wish to reproject the stills into 6-face cubes using bilinear interpolation. You will write
the results in a subfolder called `stills` and use a prefix `walk`.

.. code-block:: console

    $ odmax -r -m bilinear -s 0 -e 1 -d 5 -p "walk" -i "/home/random_user/videos/a_walk_in_the_park.mp4" -o "stills/home/random_user/videos/"

.. note::
    Please make sure that path names and prefixes are always placed between quote signs such as
    `"/home/some user/some file"`. If you do not apply quote signs and the path contains spaces, the path will not be
    parsed correctly.