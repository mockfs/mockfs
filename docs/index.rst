========================================================
:mod:`mockfs` -- A simple mock filesystem for unit tests
========================================================

`mockfs` makes it possible to test filesystem-dependent code by
replacing functions from the :mod:`os` and :mod:`glob` modules.

.. toctree::
   :maxdepth: 1

   history


Example Unit Test
=================

.. code-block:: python

    import os
    import unittest

    import mockfs


    def test_context_manager():
        """The MockFS class can be used as context manager"""
        with mockfs.MockFS(entries={'/tmp/does/not/exist': 'mockfs'}) as mfs:
            assert os.path.exists('/tmp/does/not/exist')
            with open('/tmp/does/not/exist', 'r', encoding='utf-8') as fh:
                content = fh.read()
            assert content == 'mockfs'
            mfs.add_entries({'/tmp/does/not/exist-2': 'mockfs'})
            assert os.path.exists('/tmp/does/not/exist-2')
        # Context manager scope ends: everything is back to normal now.
        assert not os.path.exists('/tmp/does/not/exist')
        assert not os.path.exists('/tmp/does/not/exist-2')


    class ExampleTestCase(unittest.TestCase):
        """The mockfs module can be used in setUp() and tearDown()"""
        def setUp(self):
            self.mfs = mockfs.replace_builtins()
            self.mfs.add_entries({'/usr/bin/mockfs-magic': 'magic'})

        def tearDown(self):
            mockfs.restore_builtins()

        def test_using_os_path(self):
            self.assertEqual(os.listdir('/usr/bin'), ['mockfs-magic'])

        def test_using_open(self):
            fh = open('/usr/bin/mockfs-magic')
            content = fh.read()
            fh.close()
            self.assertEqual(data, 'magic')


Currently supported functions:

* :func:`open`
* :func:`glob.glob`
* :func:`os.chdir`
* :func:`os.getcwd`
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


Developer Documentation
=======================

.. toctree::
   :maxdepth: 3

   api
   history

.. automodule:: mockfs
   :members:
   :undoc-members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
