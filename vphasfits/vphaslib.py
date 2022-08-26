"""
vphaslib
========

This is a simple module which allows to
convert fits from VPHAS+ project.

Provides three functions:
    1. get a single pawprint from a multi-extension fits image
    2. import a fits source table to a text file
    3. import a fits catalog to a text file
"""
from pathlib import Path
from typing import List, Optional

from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.io.fits.fitsrec import FITS_rec
from numpy import float32, isnan

header_keys = [
    "CRVAL1",
    "CRVAL2",
    "CRPIX1",
    "CRPIX2",
    "CTYPE1",
    "CTYPE2",
    "CD1_1",
    "CD2_1",
    "CD1_2",
    "CD2_2",
    "RAZP02",
    "DECZP02",
    "STDCRMS",
    "WCSPASS",
]

source_table_keys = [
    "Sequence_number",
    "RA",
    "DEC",
    "X_coordinate",
    "Y_coordinate",
    "Peak_height",
    "Peak_height_err",
    "Aper_flux_3",
    "Aper_flux_3_err",
]

catalog_keys = [
    "sourceID",
    "RAJ2000",
    "DEJ2000",
    "u",
    "err_u",
    "g",
    "err_g",
    "r2",
    "err_r2",
    "ha",
    "err_ha",
    "r",
    "err_r",
    "i",
    "err_i",
]


def make_txt_src_table_filename(src_table_fits: str, pawprint_number: int) -> str:
    """Prepare default name for text file which stores source table."""
    suffix = ".fits"
    file = Path(src_table_fits)

    if file.suffix != suffix:
        src_table_fits = str(file.with_suffix(suffix))

    return src_table_fits.replace(".fits", f"-p{pawprint_number}-srctbl.dat")


def generate_txt_header(keys: List[str]) -> str:
    """Generate a header for output text file based on data keys."""
    return f"# {' '.join(keys)}\n"


def generate_source_table_format(keys: List[str]) -> str:
    """Generate a formatter for text source table based on length of keys list."""
    return f'{("%12s " * len(keys)).rstrip(" ")}\n'


def get_fits_records(source_table_fits: str, pawprint: int) -> FITS_rec:
    """Get records from source table FITS file."""
    with fits.open(source_table_fits) as hdu_descriptor:
        records = hdu_descriptor[pawprint].data

    return records


def convert_ra_to_hhmmss(value: float, unit: Optional[str] = "deg") -> str:
    """Convert RA to hh:mm:ss format."""
    coo = SkyCoord(value, 0.0, frame="icrs", unit=unit)
    ra = coo.ra
    return f"{ra.hms[0]:02.0f}:{ra.hms[1]:02.0f}:{ra.hms[2]:06.3f}"


def convert_dec_to_ddmmss(value: float, unit: Optional[str] = "deg") -> str:
    """Convert DEC to hh:mm:ss format."""
    coo = SkyCoord(0.0, value, frame="icrs", unit=unit)
    dec = coo.dec
    if all(map(lambda x: x >= 0, dec.dms)):
        return f" {dec.dms[0]:02.0f}:{abs(dec.dms[1]):02.0f}:{abs(dec.dms[2]):05.2f}"
    else:
        return f"{dec.dms[0]:+03.0f}:{abs(dec.dms[1]):02.0f}:{abs(dec.dms[2]):05.2f}"


def make_txt_catalog_filename(catalog_fits: str) -> str:
    """Prepare default name for text file which stores catalog converted from FITS format."""
    suffix = ".fits"
    file = Path(catalog_fits)

    if file.suffix != suffix:
        catalog_fits = str(file.with_suffix(suffix))

    return catalog_fits.replace(".fits", "-cat.dat")


def generate_catalog_format(keys: List[str]) -> str:
    """Generate a formatter for text catalog based on length of keys list."""
    return f'{("%15s " * len(keys)).rstrip(" ")}\n'


def get_catalog_fits_records(catalog_fits: str) -> FITS_rec:
    """Get records from catalog FITS file."""
    with fits.open(catalog_fits) as hdu_descriptor:
        records = hdu_descriptor[1].data

    return records


def pawprint_to_fits(filename, pawprint_number):
    """Save the specific pawprint to a single fits image.

    Parameters
    ----------
    filename : str
        A name of a multi-extension fits image
        from the VPHAS+ project.
    pawprint_number : int
        A number indicating the specific pawprint.
        Valid values: 1, 2, ..., 32.

    Notes
    -----
    File is saved in the working directory
    and its name contains a proper pawprint
    number which the file comes from.
    To add/remove values of the header fits,
    please edit 'header_keys' (list) variable.

    Examples
    --------
    >>> from vphasfits import vphaslib
    >>> vphaslib.header_keys += ['PSF_FWHM']
    >>> vphaslib.pawprint_to_fits("0800b.fits", 7)
    """
    try:
        with pyfits.open(filename) as hdulist:
            try:
                pawprint_number_fits = pyfits.PrimaryHDU(hdulist[pawprint_number].data)
            except IndexError:
                print("Module %s: %i is an incorrect value of pawprint_number." % (__name__, pawprint_number))
                return

            output_name = filename.replace('.fits', '-p' + str(pawprint_number) + '.fits')
            pawprint_number_fits = pyfits.PrimaryHDU(hdulist[pawprint_number].data)
            pawprint_number_fits.header = hdulist[0].header
            del pawprint_number_fits.header['EXTEND']

            for key in header_keys:
                try:
                    pawprint_number_fits.header[key] = hdulist[pawprint_number].header[key]
                    pawprint_number_fits.header.comments[key] = hdulist[pawprint_number].header.comments[key]
                except KeyError:
                    print("Module %s: Key '%s' cannot exist in the header_keys list." % (__name__, key))
                    return

            pawprint_number_fits.header['OBJECT'] = output_name.replace(".fits","")

            try:
                pawprint_number_fits.writeto(output_name)
            except IOError as error:
                print("Module %s: %s." % (__name__, str(error)))

    except IOError:
        print("Module %s: Cannot open '%s' file." % (__name__, filename))
        return


def convert_src_table_fits_to_txt(
    src_table_fits: str, pawprint_number: int, src_table_txt: Optional[str] = None
) -> None:
    """
    Save a source table with raw data in FITS format to a text file.

    Parameters
    ----------
    src_table_fits : str
        Name (or path) of the file with multi-extension
        fits source table from the VPHAS+ project.
    pawprint_number : int
        A number indicating the specific pawprint.
        Valid values are from 1 to 32.
    src_table_txt : str, optional
        Name (or path) of the output file which stores
        source table in ASCII format. The default is None.
        If None the name of the output file contains a proper
        pawprint number which the file comes from and the
        "-srctbl.dat" suffix.


    Notes
    -----
    To add/remove columns to/from the text file, please
    edit "source_table_keys" list. This also allows to change
    the order of columns.

    Examples
    --------
    >>> from vphasfits import convert_src_table_fits_to_txt, source_table_keys
    >>> source_table_keys.remove("DEC")
    >>> source_table_keys += ['Aper_flux_4', 'Aper_flux_4_err']
    >>> convert_src_table_fits_to_txt("0704a.fits", 23)  # Output file: 0704a-p23-srctbl.dat
    """
    if src_table_txt is None:
        src_table_txt = make_txt_src_table_filename(src_table_fits, pawprint_number)

    src_table_header = generate_txt_header(source_table_keys)
    src_table_format = generate_source_table_format(source_table_keys)
    records = get_fits_records(src_table_fits, pawprint_number)

    with open(src_table_txt, "w") as file_descriptor:
        file_descriptor.write(src_table_header)

        for record in records:
            row = ()
            for key in source_table_keys:
                if key == "RA":
                    row += (convert_ra_to_hhmmss(record.field(key), "radian"),)
                elif key == "DEC":
                    row += (convert_dec_to_ddmmss(record.field(key), "radian"),)
                else:
                    row += (record.field(key),)

            file_descriptor.write(src_table_format % row)


def convert_catalog_fits_to_txt(catalog_fits: str, catalog_txt: Optional[str] = None) -> None:
    """
    Save a catalog with raw data in FITS format to a text file.

    Parameters
    ----------
    catalog_fits : str
        Name (or path) of the file with multi-extension
        fits catalog from the VPHAS+ project.
    catalog_txt : str, optional
        Name (or path) of the output file which stores
        catalog in ASCII format. The default is None.
        If None the name of the output file has the same
        name as input file with "-cat.dat" suffix.


    Notes
    -----
    To add/remove columns to/from the text file, please
    edit "catalog_keys" list. This also allows to change
    the order of columns.

    Examples
    --------
    >>> from vphasfits import convert_catalog_fits_to_txt, catalog_keys
    >>> catalog_keys.remove('sourceID')
    >>> catalog_keys
    >>> ['RAJ2000', 'DEJ2000', 'u', 'err_u', 'g', 'err_g', 'r2', 'err_r2', 'ha', 'err_ha', 'r', 'err_r', 'i', 'err_i']
    >>> convert_catalog_fits_to_txt("VPHASDR2_PSC_L213_B-1.fits")  # Output file: VPHASDR2_PSC_L213_B-1-cat.dat
    """
    if catalog_txt is None:
        catalog_txt = make_txt_catalog_filename(catalog_fits)

    catalog_header = generate_txt_header(catalog_keys)
    catalog_format = generate_catalog_format(catalog_keys)
    records = get_catalog_fits_records(catalog_fits)

    with open(catalog_txt, "w") as file_descriptor:
        file_descriptor.write(catalog_header)

        for record in records:
            row = ()
            for key in catalog_keys:
                if key == "RAJ2000":
                    row += (convert_ra_to_hhmmss(record.field(key)),)
                elif key == "DEJ2000":
                    row += (convert_dec_to_ddmmss(record.field(key)),)
                else:
                    field = record.field(key)
                    if isinstance(field, float32) and isnan(field):
                        field = 99.9999
                    row += (field,)

            file_descriptor.write(catalog_format % row)
