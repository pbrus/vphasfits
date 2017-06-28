#!/usr/bin/env python

from setuptools import setup


setup(
    name='vphas',
    description='Tools for VPHAS+ fits',
    author='Przemyslaw Brus',
    license='MIT',
    py_modules = ['pbrus.vphas.vphas'],
    install_requires=[
        'pyfits',
        'numpy',
        'math',
        'astropy',
    ],
)
