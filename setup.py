#-*- coding: utf-8 -*-
from distutils.core import setup

setup(
  name = 'vphasfits',
  version = '0.1',
  description = 'A library allows to get data from the multi-extension VPHAS+ fits',
  install_requires=['pyfits',
                    'numpy',
                    'astropy'
                    ],
  author = 'Przemysław Bruś',
  license='MIT',
  url = 'https://github.com/pbrus/vphasfits',
  download_url = 'https://github.com/pbrus/vphasfits/archive/0.1.tar.gz',
  packages = ['vphasfits'],
  keywords = ['VPHAS+', 'fits', 'text'],
  classifiers = [],
)
