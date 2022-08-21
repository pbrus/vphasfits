from io import StringIO
from unittest.mock import patch

import pytest

from vphasfits.vphaslib import (
    convert_dec_to_ddmmss,
    convert_ra_to_hhmmss,
    convert_src_table_fits_to_txt,
    generate_source_table_format,
    generate_source_table_header,
    get_fits_records,
    make_txt_src_table_filename,
)

from .fits_stubs import FITSRecordStub, HDUListStub


@pytest.fixture
def fits_open_mock():
    with patch("vphasfits.vphaslib.fits.open") as mock:
        mock.return_value.__enter__.return_value = HDUListStub()
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


# -------------------------------- TESTS --------------------------------


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
def test_generate_source_table_header(keys, result):
    assert generate_source_table_header(keys) == result


@pytest.mark.parametrize(
    "keys, result",
    [
        (["A"], "%12s\n"),
        (["A", "B", "C"], "%12s %12s %12s\n"),
    ],
)
def test_generate_source_table_format(keys, result):
    assert generate_source_table_format(keys) == result


def test_get_fits_records(fits_open_mock):
    records = get_fits_records("file.fits", 3)

    for record in records:
        assert record == FITSRecordStub()


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
def test_convert_ra_to_hhmmss(ra, result):
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
def test_convert_dec_to_ddmmss(dec, result):
    assert convert_dec_to_ddmmss(dec, "radian") == result


def test_convert_src_table_fits_to_txt(fits_open_mock, open_mock):
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


def test_convert_src_table_fits_to_txt_default_output(fits_open_mock, make_txt_src_table_filename_mock):
    fits, pawprint = "0704b.fits", 3
    convert_src_table_fits_to_txt(fits, pawprint)

    make_txt_src_table_filename_mock.assert_called_once_with(fits, pawprint)


def test_convert_src_table_fits_to_txt_passing_output(fits_open_mock, open_mock, make_txt_src_table_filename_mock):
    fits, pawprint = "0704b.fits", 4
    convert_src_table_fits_to_txt(fits, pawprint, "output_srctbl.txt")

    make_txt_src_table_filename_mock.assert_not_called()
