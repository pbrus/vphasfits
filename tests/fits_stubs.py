__all__ = ["FITSRecordStub", "FITSRecStub", "BinTableHDUStub", "HDUListStub"]


class FITSRecordStub:

    fields = {
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

    def field(self, key):
        return self.fields[key]

    def __iter__(self):
        return iter(self.fields.values())

    def __repr__(self):
        return f"{tuple([i for i in self.fields.values()])}"

    def __eq__(self, other):
        return self.fields == other.fields


class FITSRecStub:
    records_number = 2

    def __getitem__(self, i):
        if i >= self.records_number:
            raise StopIteration

        return FITSRecordStub()

    def __repr__(self):
        return f"{[self.__getitem__(i) for i in range(self.records_number)]}"


class BinTableHDUStub:
    data = FITSRecStub()

    def __getitem__(self, i):
        return self.data


class HDUListStub:
    def __getitem__(self, i):
        return BinTableHDUStub()
