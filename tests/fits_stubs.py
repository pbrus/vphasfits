from dataclasses import dataclass
from typing import Any, Dict

from numpy import array, dtype, float32, nan

__all__ = [
    "FITSRecordCatalog",
    "FITSRecordTable",
    "HDUListCatalog",
    "HDUListImgStub",
    "HDUListTable",
    "Header",
    "ImageHDUStub",
]

NaN = float32(nan)


src_table_fields = {
    "Sequence_number": 1.0,
    "RA": 4.235,
    "DEC": -0.023,
    "X_coordinate": 43.135,
    "Y_coordinate": 12.938,
    "Peak_height": 83.348,
    "Peak_height_err": 0.305,
    "Aper_flux_3": 15.913,
    "Aper_flux_3_err": 0.409,
}

catalog_fields = {
    "sourceID": "0222b-4-68296",
    "RAJ2000": 275.695,
    "DEJ2000": -30.812,
    "u": NaN,
    "err_u": NaN,
    "g": 22.754,
    "err_g": 0.163,
    "r2": 20.495,
    "err_r2": 0.091,
    "ha": 19.827,
    "err_ha": 0.101,
    "r": 20.047,
    "err_r": 0.059,
    "i": 19.147,
    "err_i": 0.053,
}

primary_header = {"OBJECT": "M13", "RA": 250.42183, "DEC": 36.45986, "EXTEND": True}

primary_comments = {
    "OBJECT": "NGC6205",
    "RA": "# Image center (RA)",
    "DEC": "# Image center (DEC)",
    "EXTEND": "Extension file",
}

image_header = {
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

image_comments = {
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


class FITSRecordStub:
    def __init__(self, fields):
        self.fields = fields

    def field(self, key):
        return self.fields[key]

    def __iter__(self):
        return iter(self.fields.values())

    def __repr__(self):
        return f"{tuple([i for i in self.fields.values()])}"

    def __eq__(self, other):
        return self.fields == other.fields


class FITSRecStub:
    def __init__(self, fields):
        self.fields = fields
        self.records_number = 2

    def __getitem__(self, i):
        if i >= self.records_number:
            raise StopIteration

        return FITSRecordStub(self.fields)

    def __repr__(self):
        return f"{[self.__getitem__(i) for i in range(self.records_number)]}"


class BinTableHDUStub:
    def __init__(self, fields):
        self.data = FITSRecStub(fields)

    def __getitem__(self, i):
        return self.data


class HDUListStub:
    def __init__(self, fields):
        self.fields = fields

    def __getitem__(self, i):
        return BinTableHDUStub(self.fields)


@dataclass
class Header:

    header: Dict[str, Any]
    comments: Dict[str, str]

    def __getitem__(self, key):
        return self.header[key]

    def __setitem__(self, key, value):
        self.header[key] = value

    def __iter__(self):
        return iter(self.header)

    def __delitem__(self, key):
        del self.header[key]
        del self.comments[key]


class PrimaryHDUStub:
    header = Header(primary_header, primary_comments)


class ImageHDUStub:
    header = Header(image_header, image_comments)
    data = array([[1, 2], [3, 4]], dtype=dtype(">i4"))


class HDUListImgStub:
    def __getitem__(self, i):
        if i == 0:
            return PrimaryHDUStub()
        else:
            return ImageHDUStub()


FITSRecordTable = FITSRecordStub(src_table_fields)
FITSRecordCatalog = FITSRecordStub(catalog_fields)
HDUListTable = HDUListStub(src_table_fields)
HDUListCatalog = HDUListStub(catalog_fields)
