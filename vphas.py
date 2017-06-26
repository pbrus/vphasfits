from __future__ import division, absolute_import, print_function

try:
    import pyfits
    from numpy import float32
    from math import isnan
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

catalog_keys = [
    'sourceID',
    'RAJ2000',
    'DEJ2000',
    'u', 'err_u',
    'g', 'err_g',
    'r2', 'err_r2',
    'ha', 'err_ha',
    'r', 'err_r',
    'i', 'err_i'
]


def pawprint_to_fits(filename, pawprint_number):
    """Save the specific pawprint to a single fits image.

    Parameters
    ----------
    filename : str
        a name of a multi-extension fits image
        from the VPHAS+ project
    pawprint_number : int
        a number indicating the specific pawprint
        Valid values: 1, 2, ..., 32

    Notes
    -----
    File is saved in the working directory
    and its name contains a proper pawprint
    number which the file comes from.
    To add/remove values of the header fits,
    please edit 'header_keys' (list) variable.

    Examples
    --------
    >>> import vphas
    >>> vphas.header_keys += ['PSF_FWHM']
    >>> vphas.pawprint_to_fits("0800b.fits", 7)
    """
    try:
        hdulist = pyfits.open(filename)
    except IOError:
        print("Module %s: Cannot open '%s' file." % (__name__, filename))
        return

    try:
        pawprint_number_fits = pyfits.PrimaryHDU(hdulist[pawprint_number].data)
    except IndexError:
        print("Module %s: %i is incorrect value of pawprint_number." % (__name__, pawprint_number))
        return

    output_name = filename.replace('.fits', '-t' + str(pawprint_number) + '.fits')
    pawprint_number_fits = pyfits.PrimaryHDU(hdulist[pawprint_number].data)
    pawprint_number_fits.header = hdulist[0].header
    del pawprint_number_fits.header['EXTEND']

    for key in header_keys:
        pawprint_number_fits.header[key] = hdulist[pawprint_number].header[key]
        pawprint_number_fits.header.comments[key] = hdulist[pawprint_number].header.comments[key]

    pawprint_number_fits.header['OBJECT'] = output_name.replace(".fits","")

    try:
        pawprint_number_fits.writeto(output_name)
    except IOError as error:
        print(str(error))
    finally:
        hdulist.close()


def srctbl_to_txt(filename, pawprint_number):
    """Save a table with raw data to a text file.

    Parameters
    ----------
    filename : str
        a name of a multi-extension fits source
        table from the VPHAS+ project
    pawprint_number : int
        a number indicating the specific pawprint
        Valid values: 1, 2, ..., 32

    Notes
    -----
    File is saved in the working directory
    and its name contains a proper pawprint
    number which the file comes from and the
    '-srctbl' suffix. To add/remove columns
    to/from the text file, please edit
    'srctbl_keys' (list) variable. This also
    allows to change the order of columns.

    Examples
    --------
    >>> import vphas
    >>> vphas.srctbl_keys.remove('DEC')
    >>> vphas.srctbl_keys += ['Aper_flux_4', 'Aper_flux_4_err']
    >>> vphas.srctbl_to_txt("0704a.fits", 23)
    """
    try:
        hdulist = pyfits.open(filename)
    except IOError:
        print("Module %s: Cannot open '%s' file." % (__name__, filename))
        return

    try:
        data = hdulist[pawprint_number].data
    except IndexError:
        print("Module %s: %i is incorrect value of pawprint_number." % (__name__, pawprint_number))
        return

    textfile_name = filename.replace('.fits', '-t' + str(pawprint_number) + '-srctbl.dat')
    textfile_descriptor = open(textfile_name, 'w')
    textfile_header = "#"

    for key in srctbl_keys:
        textfile_header += "  " + key

    textfile_descriptor.write(textfile_header + "\n")
    row_format = ("%12s " * len(srctbl_keys)).rstrip(' ') + "\n"

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


def catalog_to_txt(filename):
    """Save the VPHAS+ catalog to a text file.

    Parameters
    ----------
    filename : str
        a name of a multi-extension fits
        catalog from the VPHAS+ project

    Notes
    -----
    File is saved in the working directory
    and its name contains the '-cat' suffix.
    To add/remove columns to/from the text file,
    please edit 'catalog_keys' (list) variable.
    This also allows to change the order of columns.

    Examples
    --------
    >>> import vphas
    >>> vphas.catalog_keys.remove('sourceID')
    >>> vphas.catalog_keys
    >>> ['RAJ2000', 'DEJ2000', 'u', 'err_u', 'g', 'err_g', 'r2', 'err_r2', 'ha', 'err_ha', 'r', 'err_r', 'i', 'err_i']
    >>> vphas.catalog_to_txt("0854b.fits")
    """
    try:
        hdulist = pyfits.open(filename)
    except IOError:
        print("Module %s: Cannot open '%s' file." % (__name__, filename))
        return

    data = hdulist[1].data
    textfile_name = filename.replace('.fits', '-cat.dat')
    textfile_descriptor = open(textfile_name, 'w')
    textfile_header = "#"

    for key in catalog_keys:
        textfile_header += "  " + key

    textfile_descriptor.write(textfile_header + "\n")
    row_format = ("%15s " * len(catalog_keys)).rstrip(' ') + "\n"

    for dat in data:
        row = tuple()
        for key in catalog_keys:
            try:
                if key == "RAJ2000":
                    coo = SkyCoord(dat.field(key), 0.0, frame="icrs", unit="deg")
                    ra = "%02d:%02d:%05.2f" % (coo.ra.hms[0], coo.ra.hms[1], coo.ra.hms[2])
                    row += ra,
                elif key == "DEJ2000":
                    coo = SkyCoord(0.0, dat.field(key), frame="icrs", unit="deg")
                    dec = "%02d:%02d:%05.2f" % (coo.dec.dms[0], abs(coo.dec.dms[1]), abs(coo.dec.dms[2]))
                    row += dec,
                else:
                    df = dat.field(key)
                    if isinstance(df, float32) and isnan(df):
                        df = 99.9999
                    row += df,
            except KeyError:
                print("Module %s: Key '%s' doesn't exist." % (__name__, key))
                return
        textfile_descriptor.write(row_format % row)

    textfile_descriptor.close()
    hdulist.close()
