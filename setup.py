#!/usr/bin/env python
#
# Copyright (C) 2009, 2010 David Aguilar (davvid -at- gmail.com)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.


import sys
import mockfs
import mockfs.mfs

from distutils.core import setup


SETUP_ARGS = dict(
    name='mockfs',
    version=mockfs.__version__,
    description='Mock filesystem implementation for unit tests',
    long_description=mockfs.mfs.__doc__,
    author='David Aguilar',
    author_email='davvid@gmail.com',
    url='http://github.com/davvid/mockfs',
    license='BSD',
    platforms=['POSIX', 'Windows'],
    keywords=['unittest', 'mockfs', 'filesystem'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python'
    ],
    options={'clean': {'all': 1}},
    packages=['mockfs'],
)


def main():
    setup(**SETUP_ARGS)
    return 0


if __name__ == '__main__':
    sys.exit(main())
