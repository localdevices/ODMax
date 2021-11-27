Installation
============

User install
------------

ODMax can be installed with pip install.

To install ODMax open a console, activate a python virtual environment if you wish and do:

.. code-block:: console

    $ pip install git+https://github.com/localdevices/ODMax.git

This will install the library, API and command-line utility of ODMax.

Developer install
------------------
If you want to download ODMax directly from git to easily have access to the latest developments or
make changes to the code you can use the following steps.

First, clone ODMax's ``git`` repo from
`github <https://github.com/localdevices/ODMax.git>`_, then navigate into the
the code folder:

.. code-block:: console

    $ git clone https://github.com/localdevices/ODMax.git
    $ cd ODMax

Then, make and activate a new python environment if you wish, or use your base environment.
After that, build and install hydromt using pip as developer.

.. code-block:: console

    $ pip install -e .
