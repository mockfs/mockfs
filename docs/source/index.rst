.. mockfs documentation master file, created by
   sphinx-quickstart on Thu Dec 10 19:55:42 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================================
:mod:`mockfs` -- A simple mock filesystem for unit tests
========================================================

`mockfs` makes it possible to test filesystem-dependent code by
replacing functions from the ``os`` and ``glob`` modules.


Example Unit Test
=================

.. doctest::

    >>> import mockfs
    >>> mfs = mockfs.install()

    >>> import os
    >>> os.path.exists('/usr')
    False

    >>> mfs.add_entries({'/usr/bin/mockfs-magic': ''})
    >>> os.path.exists('/usr')
    True

    >>> os.listdir('/usr/bin')
    ['mockfs-magic']

    >>> mockfs.uninstall()
    >>> os.path.exists('/usr/bin/mockfs-magic')
    False

.. autofunction:: mockfs.install

.. autofunction:: mockfs.uninstall


Developer Documentation
=======================

.. toctree::
    :maxdepth: 3

    api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
