#!/usr/bin/env python
# coding=utf-8

try:
    from vphas import pawprint_to_fits
    from argparse import ArgumentParser
    from argparse import RawTextHelpFormatter as tefo
except ImportError as error:
    print(str(error))
    exit(1)

argparser = ArgumentParser(prog='vphas_tile.py', description='>> Program gets a specific \
tile from the multiframe VPHAS+ fits image <<', epilog='Copyright (c) 2017 Przemysław Bruś', formatter_class=tefo)
argparser.add_argument('table', help='a full name of the fits mosaic', type=str)
argparser.add_argument('tile', help='a number pointing the proper tile of the mosaic\n\
Allowed values range from 1 to 32.', type=int)
argparser.add_argument('-v', '--version', action='version', version='%(prog)s\n * Version: 2017-06-23\n \
* Licensed under the MIT license:\n   http://opensource.org/licenses/MIT\n * Copyright (c) 2017 Przemysław Bruś')
args = argparser.parse_args()

pawprint_to_fits(args.table, args.tile)
