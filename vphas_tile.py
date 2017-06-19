#!/usr/bin/env python
# coding=utf-8

import pyfits
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as tefo

keys_vphas_tile = [
'CRVAL1','CRVAL2',
'CRPIX1','CRPIX2',
'CTYPE1','CTYPE2',
'CD1_1','CD2_1',
'CD1_2','CD2_2',
'RAZP02','DECZP02',
'STDCRMS','WCSPASS'
]

def get_vphas_tile(filename, tile):
    try:
        hdulist = pyfits.open(filename)
    except IOError:
        print "Cannot open %s file!" % filename
        exit(0)

    try:
        tile_fits = pyfits.PrimaryHDU(hdulist[tile].data)
    except IndexError:
        print "%i is incorrect value of tile!" % tile
        exit(0)

    tile_fits.header = hdulist[0].header
    del tile_fits.header['EXTEND']
    for key in keys_vphas_tile:
        tile_fits.header[key] = hdulist[tile].header[key]
        tile_fits.header.comments[key] = hdulist[tile].header.comments[key]

    tile_fits = pyfits.PrimaryHDU(hdulist[tile].data)
    output_name = filename.replace('.fits', '-t' + str(tile) + '.fits')





argparser = ArgumentParser(prog='vphas_tile.py', description='>> Program gets a specific \
tile from the multiframe VPHAS+ fits image.', epilog='Author: P.Bruś, ver. 2017-03-15', formatter_class=tefo)
argparser.add_argument('cat', help='the name of the fits image')
argparser.add_argument('tile', help='the number pointing the proper tile of the vphas+ mosaic', type=int)
args = argparser.parse_args()

tile = abs(args.tile)
hdulist = get_vphas_tile(args.cat,tile)


tilefts.header['OBJECT'] = out.replace(".fits","");
tilefts.writeto(out)
hdulist.close()
