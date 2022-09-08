"""
This module allows to play with FITS data
from VPHASplus project https://www.vphasplus.org

Provides three functions:
  - Get a single pawprint from a MEF image
  - Convert FITS source table to a text file
  - Convert FITS catalog to a text file

"""
from pathlib import Path
from typing import List, Optional

from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.io.fits import PrimaryHDU
from astropy.io.fits.fitsrec import FITS_rec
from numpy import float32, isnan

image_header_keys = [
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


def make_output_fits_filename(multi_extension_fits_filename: str, pawprint_number: int) -> str:
    """Prepare default name of FITS file which stores single pawprint from MEF file."""
    suffix = ".fits"
    file = Path(multi_extension_fits_filename)

    if file.suffix != suffix:
        multi_extension_fits_filename = str(file.with_suffix(suffix))

    return multi_extension_fits_filename.replace(".fits", f"-p{pawprint_number}.fits")


def create_single_fits(multi_extension_fits_filename: str, pawprint_number: int) -> PrimaryHDU:
    """Create a single FITS image based on MEF file."""
    with fits.open(multi_extension_fits_filename) as hdu_descriptor:
        single_fits = PrimaryHDU(hdu_descriptor[pawprint_number].data)
        single_fits.header = hdu_descriptor[0].header

        for key in image_header_keys:
            single_fits.header[key] = hdu_descriptor[pawprint_number].header[key]
            single_fits.header.comments[key] = hdu_descriptor[pawprint_number].header.comments[key]

        single_fits.header["OBJECT"] += f"-p{pawprint_number}"
        del single_fits.header["EXTEND"]

    return single_fits


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


def get_source_table_fits_records(source_table_fits: str, pawprint: int) -> FITS_rec:
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


def pawprint_from_mef(
    multi_extension_fits_filename: str, pawprint_number: int, output_fits_filename: Optional[str] = None
):
    """
    Save a specific pawprint from MEF file to a single FITS image.

    Parameters
    ----------
    multi_extension_fits_filename : str
        Name (or path) of the file with multi-extension
        fits images from the VPHAS+ project.
    pawprint_number : int
        A number indicating the specific pawprint.
        Valid values are from 1 to 32.
    output_fits_filename : str, optional
        Name (or path) of the output file which stores
        a single image FITS. The default is None.
        If None the name of the output file contains a proper
        pawprint number which the file comes from.


    Notes
    -----
    To add/remove columns to/from the header FITS,
    please edit "image_header_keys" list.

    Examples
    --------
    >>> from vphasfits import pawprint_from_mef, image_header_keys
    >>> image_header_keys += ["PSF_FWHM"]
    >>> pawprint_from_mef("0800b.fits", 7)  # Output file: 0800b-p7.fits
    """
    if output_fits_filename is None:
        output_fits_filename = make_output_fits_filename(multi_extension_fits_filename, pawprint_number)

    output_fits = create_single_fits(multi_extension_fits_filename, pawprint_number)
    output_fits.writeto(output_fits_filename)


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
    >>> source_table_keys += ["Aper_flux_4", "Aper_flux_4_err"]
    >>> convert_src_table_fits_to_txt("0704a.fits", 23)  # Output file: 0704a-p23-srctbl.dat
    """
    if src_table_txt is None:
        src_table_txt = make_txt_src_table_filename(src_table_fits, pawprint_number)

    src_table_header = generate_txt_header(source_table_keys)
    src_table_format = generate_source_table_format(source_table_keys)
    records = get_source_table_fits_records(src_table_fits, pawprint_number)

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
    Save a catalog with data in FITS format to a text file.

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
    >>> catalog_keys.remove("sourceID")
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
