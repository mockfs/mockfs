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

    >>> import os
    >>> import mockfs

    >>> mockfs.install()
    >>> mockfs.add_entries({'/new/magic': ''})

    >>> os.path.exists('/new')
    True

    >>> os.listdir('/new')
    ['magic']

    >>> os.path.exists('/bin')
    False

    >>> mockfs.uninstall()

    >>> os.path.exists('/new')
    False

    >>> os.path.exists('/bin')
    True

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

