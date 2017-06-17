#!/usr/bin/env python
# coding=utf-8

import pyfits
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as tefo

argparser = ArgumentParser(prog='vphas_tile.py', description='>> Program gets a specific \
tile from the multiframe VPHAS+ fits image.', epilog='Author: P.Bruś, ver. 2017-03-15', formatter_class=tefo)
argparser.add_argument('cat', help='the name of the fits image')
argparser.add_argument('tile', help='the number pointing the proper tile of the vphas+ mosaic', type=int)
args = argparser.parse_args()

tile = abs(args.tile)
hdulist = pyfits.open(args.cat)
out = args.cat.replace('.fits', '-t' + str(tile) + '.fits')
tilefts = pyfits.PrimaryHDU(hdulist[tile].data)
tilefts.header = hdulist[0].header
del tilefts.header['EXTEND']
key = [
'CRVAL1','CRVAL2',
'CRPIX1','CRPIX2',
'CTYPE1','CTYPE2',
'CD1_1','CD2_1',
'CD1_2','CD2_2',
'RAZP02','DECZP02',
'STDCRMS','WCSPASS'
]

for k in key:
    tilefts.header[k] = hdulist[tile].header[k]
    tilefts.header.comments[k] = hdulist[tile].header.comments[k]

tilefts.header['OBJECT'] = out.replace(".fits","");
tilefts.writeto(out)
hdulist.close()
