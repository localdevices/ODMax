Introduction
============

What is ODMax
-------------
ODMax is a command-line interface and API to extract stills in typical image formats from 360 degree videos. It can:

- Extract frames from videos at demanded start and end times, and with specified frame intervals
- Reproject frames from spherical projections into cube-face projection
- When available in the original video, provide time stamps and GPS positions to the still images
- Store final frames with configurable paths and prefixes in files (for local) or bytestreams for cloud use.

ODMax prepares still materials from videos for downstream use cases such as:
- Image analysis such as image recognition and segmentation
- 3D photogrammetry (see also `OpenDroneMap <https://www.opendronemap.org/>`_)

We offer both a Command-Line Interface and an API. Both are fully described in this manual.

