from io import StringIO
from unittest.mock import Mock, patch

import pytest

from vphasfits.vphaslib import (
    convert_catalog_fits_to_txt,
    convert_dec_to_ddmmss,
    convert_ra_to_hhmmss,
    convert_src_table_fits_to_txt,
    create_single_fits,
    generate_catalog_format,
    generate_source_table_format,
    generate_txt_header,
    get_catalog_fits_records,
    get_source_table_fits_records,
    make_output_fits_filename,
    make_txt_catalog_filename,
    make_txt_src_table_filename,
    pawprint_from_mef,
)

from .fits_stubs import (
    FITSRecordCatalog,
    FITSRecordTable,
    HDUListCatalog,
    HDUListImgStub,
    HDUListTable,
    Header,
    ImageHDUStub,
)


@pytest.fixture
def fits_image_open_mock():
    with patch("vphasfits.vphaslib.fits.open") as mock:
        mock.return_value.__enter__.return_value = HDUListImgStub()
        yield mock


@pytest.fixture
def primary_hdu_mock():
    with patch("vphasfits.vphaslib.PrimaryHDU") as mock:
        yield mock


@pytest.fixture
def create_single_fits_mock():
    with patch("vphasfits.vphaslib.create_single_fits") as mock:
        mock.return_value = Mock()
        yield mock


@pytest.fixture
def fits_src_table_open_mock():
    with patch("vphasfits.vphaslib.fits.open") as mock:
        mock.return_value.__enter__.return_value = HDUListTable
        yield mock


@pytest.fixture
def fits_catalog_open_mock():
    with patch("vphasfits.vphaslib.fits.open") as mock:
        mock.return_value.__enter__.return_value = HDUListCatalog
        yield mock


@pytest.fixture
def open_mock():
    with patch("vphasfits.vphaslib.open") as mock:
        mock.return_value.__enter__.return_value = StringIO()
        yield mock


@pytest.fixture
def make_txt_src_table_filename_mock():
    with patch("vphasfits.vphaslib.make_txt_src_table_filename") as mock:
        yield mock


@pytest.fixture
def make_txt_catalog_filename_mock():
    with patch("vphasfits.vphaslib.make_txt_catalog_filename") as mock:
        yield mock


# -------------------------------- TESTS --------------------------------


@pytest.mark.parametrize(
    "fits, pawprint, result",
    [
        ("ADP.2019-10-07T14:31:52.250.fits", 15, "ADP.2019-10-07T14:31:52.250-p15.fits"),
        ("my.file.fits", 3, "my.file-p3.fits"),
        ("MULTI-MATRIX", 19, "MULTI-MATRIX-p19.fits"),
        (r"/path/to/MEF_file.fits", 22, r"/path/to/MEF_file-p22.fits"),
    ],
)
def test_make_output_fits_filename(fits, pawprint, result):
    assert make_output_fits_filename(fits, pawprint) == result


def test_create_single_fits(fits_image_open_mock, primary_hdu_mock):
    pawprint = 5
    primary_hdu_mock.return_value = ImageHDUStub()
    result_header = {
        "OBJECT": f"M13-p{pawprint}",
        "RA": 250.42183,
        "DEC": 36.45986,
        "CRVAL1": 2.39,
        "CRVAL2": 10.56,
        "CRPIX1": 32.65,
        "CRPIX2": 6.38,
        "CTYPE1": "RA-TAN",
        "CTYPE2": "DEC-TAN",
        "CD1_1": 14.07,
        "CD2_1": 18.47,
        "CD1_2": 0.76,
        "CD2_2": 27.53,
        "RAZP02": 28.15,
        "DECZP02": 30.53,
        "STDCRMS": 16.73,
        "WCSPASS": 5,
    }
    result_comments = {
        "OBJECT": "NGC6205",
        "RA": "# Image center (RA)",
        "DEC": "# Image center (DEC)",
        "CRVAL1": "deg",
        "CRVAL2": "deg",
        "CRPIX1": "Center pixel",
        "CRPIX2": "Center pixel",
        "CTYPE1": "Pixel coo",
        "CTYPE2": "Pixel coo",
        "CD1_1": "WCS",
        "CD2_1": "WCS",
        "CD1_2": "WCS",
        "CD2_2": "WCS",
        "RAZP02": "RA shift",
        "DECZP02": "DEC shift",
        "STDCRMS": "RMS",
        "WCSPASS": "WCS PASS",
    }

    fits = create_single_fits("image.fits", pawprint)

    assert fits.header == Header(result_header, result_comments)
    assert (fits.data == ImageHDUStub.data).all()


def test_get_pawprint_from_mef_passing_output_filename(create_single_fits_mock):
    output = "pawprint_7.fits"
    create_single_fits_mock.return_value = Mock()
    pawprint_from_mef("mef.fits", 7, output)

    create_single_fits_mock.assert_called_once()
    create_single_fits_mock.return_value.writeto.assert_called_once_with(output)


def test_get_pawprint_from_mef_default_output_filename(create_single_fits_mock):
    create_single_fits_mock.return_value = Mock()
    pawprint_from_mef("mef.fits", 7)

    create_single_fits_mock.assert_called_once()
    create_single_fits_mock.return_value.writeto.assert_called_once_with("mef-p7.fits")


@pytest.mark.parametrize(
    "fits, pawprint, result",
    [
        ("ADP.2019-10-07T14:31:52.250.fits", 15, "ADP.2019-10-07T14:31:52.250-p15-srctbl.dat"),
        ("my.file.fits", 3, "my.file-p3-srctbl.dat"),
        ("MULTI-MATRIX", 19, "MULTI-MATRIX-p19-srctbl.dat"),
        (r"/path/to/source-table.fits", 22, r"/path/to/source-table-p22-srctbl.dat"),
    ],
)
def test_make_txt_src_table_filename(fits, pawprint, result):
    assert make_txt_src_table_filename(fits, pawprint) == result


@pytest.mark.parametrize(
    "keys, result",
    [
        (["Field1", "Field2", "Field3"], "# Field1 Field2 Field3\n"),
        (["Column1", "ParameterX", "ParameterY", "Comment"], "# Column1 ParameterX ParameterY Comment\n"),
    ],
)
def test_generate_txt_header(keys, result):
    assert generate_txt_header(keys) == result


@pytest.mark.parametrize(
    "keys, result",
    [
        (["A"], "%12s\n"),
        (["A", "B", "C"], "%12s %12s %12s\n"),
    ],
)
def test_generate_source_table_format(keys, result):
    assert generate_source_table_format(keys) == result


def test_get_source_table_fits_records(fits_src_table_open_mock):
    records = get_source_table_fits_records("file.fits", 3)

    for record in records:
        assert record == FITSRecordTable


@pytest.mark.parametrize(
    "ra, result",
    [
        (0.0, "00:00:00.000"),
        (6.283112526949778, "23:59:58.999"),
        (6.283185307179586, "00:00:00.000"),
        (3.170623413169915, "12:06:39.202"),
        (0.087269778725295, "00:20:00.046"),
        (1.572382831084959, "06:00:21.816"),
        (0.001789486082069, "00:00:24.607"),
    ],
)
def test_convert_ra_radian_to_hhmmss(ra, result):
    assert convert_ra_to_hhmmss(ra, "radian") == result


@pytest.mark.parametrize(
    "dec, result",
    [
        (-1.7453292519943297e-07, "-00:00:00.04"),
        (-0.000530929158456, "-00:01:49.51"),
        (1.5707961522619713, " 89:59:59.96"),
        (0.7871785737674077, " 45:06:07.24"),
        (3.4906585039886593e-07, " 00:00:00.07"),
    ],
)
def test_convert_dec_radian_to_ddmmss(dec, result):
    assert convert_dec_to_ddmmss(dec, "radian") == result


def test_convert_src_table_fits_to_txt(fits_src_table_open_mock, open_mock):
    result = (
        "# Sequence_number RA DEC X_coordinate Y_coordinate Peak_height Peak_height_err Aper_flux_3 Aper_flux_3_err\n"
        "         1.0 16:10:35.430 -01:19:04.09       43.135       12.938       83.348        0.305       15.913"
        "        0.409\n"
        "         1.0 16:10:35.430 -01:19:04.09       43.135       12.938       83.348        0.305       15.913"
        "        0.409\n"
    )
    convert_src_table_fits_to_txt("file.fits", 1)
    content = open_mock.return_value.__enter__.return_value
    content.seek(0)
    assert "".join(content.readlines()) == result


def test_convert_src_table_fits_to_txt_default_output(fits_src_table_open_mock, make_txt_src_table_filename_mock):
    fits, pawprint = "0704b.fits", 3
    convert_src_table_fits_to_txt(fits, pawprint)

    make_txt_src_table_filename_mock.assert_called_once_with(fits, pawprint)


def test_convert_src_table_fits_to_txt_passing_output(
    fits_src_table_open_mock, open_mock, make_txt_src_table_filename_mock
):
    fits, pawprint = "0704b.fits", 4
    convert_src_table_fits_to_txt(fits, pawprint, "output_srctbl.txt")

    make_txt_src_table_filename_mock.assert_not_called()


@pytest.mark.parametrize(
    "fits, result",
    [
        ("ADP.2019-10-07T14:31:52.250.fits", "ADP.2019-10-07T14:31:52.250-cat.dat"),
        ("objects.fits", "objects-cat.dat"),
        ("BINARY_CATALOG", "BINARY_CATALOG-cat.dat"),
        (r"/path/to/catalog.fits", r"/path/to/catalog-cat.dat"),
    ],
)
def test_make_txt_catalog_filename(fits, result):
    assert make_txt_catalog_filename(fits) == result


@pytest.mark.parametrize(
    "keys, result",
    [
        ([1], "%15s\n"),
        (["X", "Y", "Z"], "%15s %15s %15s\n"),
    ],
)
def test_generate_catalog_format(keys, result):
    assert generate_catalog_format(keys) == result


def test_get_catalog_fits_records(fits_catalog_open_mock):
    records = get_catalog_fits_records("catalog.fits")

    for record in records:
        assert record == FITSRecordCatalog


@pytest.mark.parametrize(
    "ra, result",
    [
        (0.0, "00:00:00.000"),
        (0.0001, "00:00:00.024"),
        (2.150, "00:08:36.000"),
        (130.024, "08:40:05.760"),
        (359.999, "23:59:59.760"),
        (360.000, "00:00:00.000"),
    ],
)
def test_convert_ra_deg_to_hhmmss(ra, result):
    assert convert_ra_to_hhmmss(ra) == result


@pytest.mark.parametrize(
    "dec, result",
    [
        (-90.000, "-90:00:00.00"),
        (-89.999, "-89:59:56.40"),
        (-0.001, "-00:00:03.60"),
        (0.0, " 00:00:00.00"),
        (89.9995, " 89:59:58.20"),
    ],
)
def test_convert_dec_deg_to_ddmmss(dec, result):
    assert convert_dec_to_ddmmss(dec) == result


def test_convert_catalog_fits_to_txt(fits_catalog_open_mock, open_mock):
    result = (
        "# sourceID RAJ2000 DEJ2000 u err_u g err_g r2 err_r2 ha err_ha r err_r i err_i\n"
        "  0222b-4-68296    18:22:46.800    -30:48:43.20         99.9999         99.9999          22.754"
        "           0.163          20.495           0.091          19.827           0.101          20.047"
        "           0.059          19.147           0.053\n"
        "  0222b-4-68296    18:22:46.800    -30:48:43.20         99.9999         99.9999          22.754"
        "           0.163          20.495           0.091          19.827           0.101          20.047"
        "           0.059          19.147           0.053\n"
    )
    convert_catalog_fits_to_txt("file.fits")
    content = open_mock.return_value.__enter__.return_value
    content.seek(0)
    assert "".join(content.readlines()) == result


def test_convert_catalog_fits_to_txt_default_output(fits_catalog_open_mock, make_txt_catalog_filename_mock):
    fits = "0704b.fits"
    convert_catalog_fits_to_txt(fits)

    make_txt_catalog_filename_mock.assert_called_once_with(fits)


def test_convert_catalog_fits_to_txt_passing_output(fits_catalog_open_mock, open_mock, make_txt_catalog_filename_mock):
    fits = "0704b.fits"
    convert_catalog_fits_to_txt(fits, "output_catalog.txt")

    make_txt_catalog_filename_mock.assert_not_called()
