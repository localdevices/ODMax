Our github repository contains the code (development versions) as well as several Jupyter notebook examples for ODMax.

To run these examples make sure that you have installed a complete environment including jupyter and plotting.
The easiest approach is to create a conda environment with the ``environment.yml`` contained in the root folder of our
repository available on github. Please first clone our repository and go to the repository folder with:

.. code-block:: console

  $ git clone https://github.com/localdevices/ODMax.git
  $ cd ODMax

Then create the environment and activate it

.. code-block:: console

  $ conda env create -f environment.yml
  $ conda activate odmax

Finally go to the notebook folder and start your own jupyter notebook server as follows:

.. code-block:: console

  $ cd notebooks
  $ jupyter notebook

After this, a browser window should open and the list of notebooks (with extension ``.ipynb``) appear. The same notebooks
with already executed code can be viewed in the links below.

.. toctree::
   :maxdepth: 1

