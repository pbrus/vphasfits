#!/usr/bin/env python
# coding=utf-8

try:
    from vphas import catalog_to_txt
    from argparse import ArgumentParser
    from argparse import RawTextHelpFormatter as tefo
except ImportError as error:
    print(str(error))
    exit(1)

argparser = ArgumentParser(prog='vphas_cat.py', description='>> Program transforms data \
from the VPHAS+ fits catalog to a text file <<', epilog='Copyright (c) 2017 Przemysław Bruś', formatter_class=tefo)
argparser.add_argument('catalog', help='a name of the fits catalog from VPHAS+')
argparser.add_argument('-v', '--version', action='version', version='%(prog)s\n * Version: 2017-06-26\n \
* Licensed under the MIT license:\n   http://opensource.org/licenses/MIT\n * Copyright (c) 2017 Przemysław Bruś')
args = argparser.parse_args()

catalog_to_txt(args.catalog)
