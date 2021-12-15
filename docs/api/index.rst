.. _api:

=============
API reference
=============

ODMax's API currently consists of two classes, the ``Video`` class, and the ``Frame`` class. The classes are based
on calls of functions. We highly recommend to use the two classes, as these will provide most if not all functionality
useful for extracting frames, extracting and including GPS data in frame writing, projection of 360-degree imagery
to cube-faces, plotting and writing to files. Of course you can also use the called functions for more flexibility.

.. note::
    We expect to integrate ODMax's API with WebODM in the near future. This will enable direct uploads of ODMax derived
    stills into WebODM projects. WebODM is a powerful, free and open-source web-based photogrammetry software.
    See https://www.opendronemap.org/webodm/ for more information.

In the remaining sections, we describe the API classes, and the functions they are based on.

Video class
-----------

.. automodule:: odmax.Video
    :members: __init__, get_gps, get_frame, plot_gps
    :imported-members:
    :undoc-members:
    :show-inheritance:

Frame class
-----------

.. automodule:: odmax.Frame
    :members: __init__, to_file, to_bytes, plot
    :imported-members:
    :undoc-members:
    :show-inheritance:


Input-output
------------

.. automodule:: odmax.io
    :members: to_pil, open_file, get_frame_number, read_frame, write_frame, get_gpx
    :imported-members:
    :undoc-members:
    :show-inheritance:

Processing
----------

.. automodule:: odmax.process
    :members: reproject_cube
    :imported-members:
    :undoc-members:
    :show-inheritance:

