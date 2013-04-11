#!/usr/bin/env python
#
# Copyright (C) 2009, 2010 David Aguilar (davvid -at- gmail.com)
# All rights reserved.
# Copyright (C) 2013 Canonical Limited.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.


import sys

from setuptools import setup

SETUP_ARGS = dict(
    name='mockfs',
    version="1.0.1",
    description='Mock filesystem implementation for unit tests',
    long_description="",
    author='David Aguilar',
    author_email='davvid@gmail.com',
    url='https://github.com/mockfs/mockfs',
    license='BSD',
    platforms=['POSIX', 'Windows'],
    keywords=['unittest', 'mockfs', 'filesystem'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python'
    ],
    options={'clean': {'all': 1}},
    packages=['mockfs', 'mockfs.tests'],
    use_2to3=True,
    test_suite='mockfs.tests.suite',
)


def main():
    setup(**SETUP_ARGS)
    return 0


if __name__ == '__main__':
    sys.exit(main())
