#!/usr/bin/env python
# coding=utf-8

import pyfits
import numpy as np
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as tefo
from astropy import units as u
from astropy.coordinates import SkyCoord
from math import isnan

argparser = ArgumentParser(prog='vphas_cat.py', description='>> Program gets stars \
from the vphas+ FITS catalog', epilog='Author: P.Bruś, ver. 2017-01-12', formatter_class=tefo)
argparser.add_argument('cat', help='name of the fits catalog from vphas+')
args = argparser.parse_args()

hdulist = pyfits.open(args.cat)
out = args.cat.replace('fits','txt')
data = hdulist[1].data

fd = open(out, 'w')

filters = [
	'u', 'err_u',
	'g', 'err_g',
	'r2', 'err_r2',
	'ha', 'err_ha',
	'r', 'err_r',
	'i', 'err_i'
]

fd.write("#  sourceID  RAJ2000  DEJ2000")
for f in filters:
	fd.write("  " + f)
fd.write("\n")

for d in data:
	tupline = d.field("sourceID"),
	coo = SkyCoord(d.field("RAJ2000"), d.field("DEJ2000"), frame="icrs", unit="deg")
	ra = "%02d:%02d:%05.2f" % (coo.ra.hms[0],coo.ra.hms[1],coo.ra.hms[2])
	dec = "%02d:%02d:%05.2f" % (coo.dec.dms[0],abs(coo.dec.dms[1]),abs(coo.dec.dms[2]))
	tupline += ra, dec,
	for f in filters:
		val = d.field(f)
		if isinstance(val,np.float32) and isnan(val):
			val = 99.9999
		tupline += val,
	fd.write("%-14s %s %s %7.4f %7.4f %7.4f %7.4f %7.4f %7.4f %7.4f %7.4f %7.4f %7.4f %7.4f %7.4f\n" % tupline)

fd.close()
hdulist.close()
