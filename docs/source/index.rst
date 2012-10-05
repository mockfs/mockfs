.. mockfs documentation master file, created by
   sphinx-quickstart on Thu Dec 10 19:55:42 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================================
:mod:`mockfs` -- A simple mock filesystem for unit tests
========================================================

`mockfs` makes it possible to test filesystem-dependent code by
replacing functions from the :mod:`os` and :mod:`glob` modules.

Example Unit Test
=================

.. code-block:: python

    import os
    import unittest

    import mockfs

    class ExampleTestCase(unittest.TestCase):
        def setUp(self):
            self.mfs = mockfs.setup()
            self.mfs.add_entries({'/usr/bin/mockfs-magic': 'magic'})

        def tearDown(self):
            mockfs.teardown()

        def test_using_os_path(self):
            self.assertEqual(os.listdir('/usr/bin'), ['mockfs-magic'])

        def test_using_open(self):
            fh = open('/usr/bin/mockfs-magic')
            content = fh.read()
            fh.close()
            self.assertEqual(data, 'magic')

Currently supported functions:

* :func:`__builtins__.open`
* :func:`__builtins__.close`
* :func:`glob.glob`
* :func:`os.chdir`
* :func:`os.getcwd`
* :func:`os.getcwdu`
* :func:`os.listdir`
* :func:`os.makedirs`
* :func:`os.path.abspath`
* :func:`os.path.exists`
* :func:`os.path.getsize`
* :func:`os.path.islink`
* :func:`os.path.isdir`
* :func:`os.path.isfile`
* :func:`os.remove`
* :func:`os.rmdir`
* :func:`os.unlink`
* :func:`os.walk`
* :func:`shutil.rmtree`

.. autofunction:: mockfs.setup

.. autofunction:: mockfs.teardown


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
