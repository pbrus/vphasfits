from __future__ import division, absolute_import, print_function

try:
    import pyfits
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

def get_tile(filename, tile):
    try:
        hdulist = pyfits.open(filename)
    except IOError:
        print("Module %s: Cannot open %s file." % (__name__, filename))
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
