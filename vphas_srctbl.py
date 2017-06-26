#!/usr/bin/env python
# coding=utf-8

try:
    from vphas import srctbl_to_txt
    from argparse import ArgumentParser
    from argparse import RawTextHelpFormatter as tefo
except ImportError as error:
    print(str(error))
    exit(1)

argparser = ArgumentParser(prog='vphas_srctbl.py', description='>> Program transforms data \
from the VPHAS+ fits source table to a text file <<', epilog='Copyright (c) 2017 Przemysław Bruś', formatter_class=tefo)
argparser.add_argument('srctable', help='a name of the fits source table from VPHAS+')
argparser.add_argument('tile', help='a number pointing the proper tile of the mosaic\n\
Allowed values range from 1 to 32.', type=int)
argparser.add_argument('-v', '--version', action='version', version='%(prog)s\n * Version: 2017-06-26\n \
* Licensed under the MIT license:\n   http://opensource.org/licenses/MIT\n * Copyright (c) 2017 Przemysław Bruś')
args = argparser.parse_args()

srctbl_to_txt(args.srctable, args.tile)
