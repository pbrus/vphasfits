[![tests](https://github.com/pbrus/vphasfits/actions/workflows/tests.yml/badge.svg)](https://github.com/pbrus/vphasfits/actions/workflows/tests.yml)
# Vphasfits

Python 3.6+ package converting the multi-extension FITS (MEF) frames from the [**VPHASplus**](http://www.vphasplus.org) project to handy formats.

## Installation

Installation command:
```bash
$ sudo pip install git+https://github.com/pbrus/vphasfits
```
or:
```bash
$ git clone https://github.com/pbrus/vphasfits
$ cd vphasfits
$ sudo python setup.py install
```

To uninstall the package, please type from the command line:
 ```bash
$ sudo pip uninstall vphasfits
```

## Usage
### Functions

After installation you can add the library to own project or test it using interactive mode of Python:
```python
>>> from vphasfits import pawprint_from_mef, convert_src_table_fits_to_txt, convert_catalog_fits_to_txt
```
This will give you three functions to handle the data from the [ESO query interface](http://archive.eso.org/wdb/wdb/adp/phase3_main/form?phase3_collection=VPHASplus&release_tag=3):

1. get a single pawprint from a MEF image; product category: *image*
```python
>>> pawprint_from_mef("ADP.2015-05-11T10-20-21.993.fits", 7)
```
2. import source table to a text file; product category: *source_table*
```python
>>> convert_src_table_fits_to_txt("ADP.2015-05-11T10-19-46.847.fits", 23)
```
3. import catalog to a text file; product category: *catalog*
```python
>>> convert_catalog_fits_to_txt("VPHASDR2_PSC_L213_B-1.fits")
```

Data from the [**VPHASplus**](http://www.vphasplus.org) project are stored inside FITS format. You can easily choose columns or keys of header which can be used before conversion. To do this, please edit the following lists (add/remove/permutate their elements):
```python
>>> from vphasfits import image_header_keys, source_table_keys, catalog_keys
>>> image_header_keys
['CRVAL1', 'CRVAL2', 'CRPIX1', 'CRPIX2', 'CTYPE1', 'CTYPE2', 'CD1_1', 'CD2_1', 'CD1_2', 'CD2_2', 'RAZP02', 'DECZP02', 'STDCRMS', 'WCSPASS']
>>> source_table_keys
['Sequence_number', 'RA', 'DEC', 'X_coordinate', 'Y_coordinate', 'Peak_height', 'Peak_height_err', 'Aper_flux_3', 'Aper_flux_3_err']
>>> catalog_keys
['sourceID', 'RAJ2000', 'DEJ2000', 'u', 'err_u', 'g', 'err_g', 'r2', 'err_r2', 'ha', 'err_ha', 'r', 'err_r', 'i', 'err_i']
```
To see more info about the module, please call the docstring:
```python
>>> import vphasfits
>>> help(vphasfits)
```

### Scripts

The package contains also three ready-to-use programs in the `scripts/` directory. After installation the `vphasfits` module you can use them from anywhere. The `argparse` module is needed. More info can be found calling scripts with the `--help` option.

## License

**Vphasfits** is licensed under the [MIT license](http://opensource.org/licenses/MIT).
