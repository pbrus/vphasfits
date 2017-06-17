#!/usr/bin/env python
# coding=utf-8

import pyfits
import numpy as np
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as tefo
from astropy import units as u
from astropy.coordinates import SkyCoord

argparser = ArgumentParser(prog='vphas_srctbl.py', description='>> Program transforms data \
from the vphas+ FITS catalog to a txt file', epilog='Author: P.Bruś, ver. 2017-01-12', formatter_class=tefo)
argparser.add_argument('cat', help='the name of the fits catalog from vphas+')
argparser.add_argument('tile', help='the number pointing the proper tile of the vphas+ mosaic', type=int)
args = argparser.parse_args()

tile = abs(args.tile)
hdulist = pyfits.open(args.cat)
data = hdulist[tile].data
out = args.cat.replace('.fits', '-t' + str(tile) + '-srctbl.dat')
fd = open(out, 'w')

fields = [
	'X_coordinate',
	'Y_coordinate',
	'Peak_height',
	'Peak_height_err',
	'Aper_flux_3',
	'Aper_flux_3_err'
]

hdr = "#  Index  Ra  Dec"
for f in fields:
	hdr += "  " + f
fd.write(hdr + "\n")

for d in data:
	tupline = d.field("Sequence_number"),
	coo = SkyCoord(d.field("RA"), d.field("DEC"), frame="icrs", unit="radian")
	ra = "%02d:%02d:%05.2f" % (coo.ra.hms[0],coo.ra.hms[1],coo.ra.hms[2])
	dec = "%02d:%02d:%05.2f" % (coo.dec.dms[0],abs(coo.dec.dms[1]),abs(coo.dec.dms[2]))
	tupline += ra, dec,
	for f in fields:
		tupline += d.field(f),
	fd.write("%5.0lf %s %s %12.3lf %9.3lf %12.3lf %9.3lf %12.3lf %10.3lf\n" % tupline)

fd.close()
hdulist.close()
