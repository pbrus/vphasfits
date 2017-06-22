from __future__ import division, absolute_import, print_function

try:
    import pyfits
    #import numpy as np
    from astropy import units as u
    from astropy.coordinates import SkyCoord
except ImportError as error:
    print(str(error))
    exit(1)


header_keys = [
'CRVAL1','CRVAL2',
'CRPIX1','CRPIX2',
'CTYPE1','CTYPE2',
'CD1_1','CD2_1',
'CD1_2','CD2_2',
'RAZP02','DECZP02',
'STDCRMS','WCSPASS'
]

srctbl_keys = [
    'Sequence_number',
    'RA', 'DEC',
    'X_coordinate',
    'Y_coordinate',
    'Peak_height',
    'Peak_height_err',
    'Aper_flux_3',
    'Aper_flux_3_err'
]

def get_tile(filename, tile):
    try:
        hdulist = pyfits.open(filename)
    except IOError:
        print("Module %s: Cannot open '%s' file." % (__name__, filename))
        return

    try:
        tile_fits = pyfits.PrimaryHDU(hdulist[tile].data)
    except IndexError:
        print("Module %s: %i is incorrect value of tile." % (__name__, tile))
        return

    output_name = filename.replace('.fits', '-t' + str(tile) + '.fits')
    tile_fits = pyfits.PrimaryHDU(hdulist[tile].data)
    tile_fits.header = hdulist[0].header
    del tile_fits.header['EXTEND']

    for key in header_keys:
        tile_fits.header[key] = hdulist[tile].header[key]
        tile_fits.header.comments[key] = hdulist[tile].header.comments[key]

    tile_fits.header['OBJECT'] = output_name.replace(".fits","")

    try:
        tile_fits.writeto(output_name)
    except IOError as error:
        print(str(error))
    finally:
        hdulist.close()


def srctbl_to_textfile(filename, tile):
    try:
        hdulist = pyfits.open(filename)
    except IOError:
        print("Module %s: Cannot open '%s' file." % (__name__, filename))
        return

    try:
        data = hdulist[tile].data
    except IndexError:
        print("Module %s: %i is incorrect value of tile." % (__name__, tile))
        return

    textfile_name = filename.replace('.fits', '-t' + str(tile) + '-srctbl.dat')
    textfile_descriptor = open(textfile_name, 'w')
    textfile_header = "#"

    for key in srctbl_keys:
        textfile_header += "  " + key

    textfile_descriptor.write(textfile_header + "\n")
    row_format = ("%14s " * len(srctbl_keys)).rstrip(' ') + "\n"

    for dat in data:
        row = tuple()
        for key in srctbl_keys:
            try:
                if key == "RA":
                    coo = SkyCoord(dat.field(key), 0.0, frame="icrs", unit="radian")
                    ra = "%02d:%02d:%05.2f" % (coo.ra.hms[0], coo.ra.hms[1], coo.ra.hms[2])
                    row += ra,
                elif key == "DEC":
                    coo = SkyCoord(0.0, dat.field(key), frame="icrs", unit="radian")
                    dec = "%02d:%02d:%05.2f" % (coo.dec.dms[0], abs(coo.dec.dms[1]), abs(coo.dec.dms[2]))
                    row += dec,
                else:
                    row += dat.field(key),
            except KeyError:
                print("Module %s: Key '%s' doesn't exist." % (__name__, key))
                return
        textfile_descriptor.write(row_format % row)

    textfile_descriptor.close()
    hdulist.close()
