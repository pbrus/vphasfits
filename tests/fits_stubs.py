from numpy import float32, nan

__all__ = ["FITSRecordCatalog", "FITSRecordTable", "HDUListCatalog", "HDUListTable"]

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


FITSRecordTable = FITSRecordStub(src_table_fields)
FITSRecordCatalog = FITSRecordStub(catalog_fields)
HDUListTable = HDUListStub(src_table_fields)
HDUListCatalog = HDUListStub(catalog_fields)
