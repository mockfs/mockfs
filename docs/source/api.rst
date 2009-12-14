.. _mockfs-api:

.. testsetup:: *

    import mockfs

.. contents::

===============================
:mod:`mockfs` -- High Level API
===============================

.. doctest::

   >>> import mockfs
   >>> mockfs.install({'/new/entry': ''})

   >>> import os
   >>> os.path.exists('/new')
   True

   >>> mockfs.uninstall()
   >>> os.path.exists('/new')
   False


.. automodule:: mockfs
   :members:
   :undoc-members:

=============
Developer API
=============

.. automodule:: mockfs.mockfs
   :members:
   :undoc-members:


File Storage
------------
.. automodule:: mockfs.storage
   :members:
   :undoc-members:

MockFS Data Layer
-----------------
.. automodule:: mockfs.data
   :members:
   :undoc-members:
