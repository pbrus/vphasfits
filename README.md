# Vphasfits [![GitHub release](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/ver20170706.svg "download")](https://github.com/pbrus/vphasfits/) ![Written in Python](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/python.svg "language")

This module allows to convert the multi-extension *FITS* frames from the [**VPHASplus**](http://www.vphasplus.org) project to handy formats.

## Installation

This library was written in *Python2.7*. To install it, please type from the command line:
```bash
$ sudo pip install git+https://github.com/pbrus/vphasfits
```
or:
```bash
$ git clone https://github.com/pbrus/vphasfits
$ cd vphasfits
$ sudo python setup.py install
```
Additionally the module uses the following components:

 * *pytfits*
 * *numpy*
 * *math*
 * *astropy*

which should be installed automatically during the package installation. To uninstall the whole module, please type from the command line:
 ```bash
$ sudo pip uninstall vphasfits
```

## Usage

After installation you can add the library to own project or test it using interactive mode of Python:
```python
>>> from vphasfits import vphaslib
```
This will give you three functions to handle the data from the [ESO query interface](http://archive.eso.org/wdb/wdb/adp/phase3_main/form?phase3_collection=VPHASplus&release_tag=3):

1. get a single pawprint from a multi-extension fits image; product category: *image*
```python
>>> vphaslib.pawprint_to_fits("ADP.2015-05-11T10:20:21.993.fits", 7)
```
2. import a fits source table to a text file; product category: *source_table*
```python
>>> vphaslib.srctbl_to_txt("ADP.2015-05-11T10:19:46.847.fits", 23)
```
3. import a fits catalog to a text file; product category: *catalog*
```python
>>> vphaslib.catalog_to_txt("VPHASDR2_PSC_L213_B+1.fits")
```

All data from the [**VPHASplus**](http://www.vphasplus.org) project are stored inside *FITS* files. You can easly choose columns or keys of header which can be used before conversion. To do this, please edit the following lists (add/remove/permutate their elements):
```python
>>> vphaslib.header_keys
['CRVAL1', 'CRVAL2', 'CRPIX1', 'CRPIX2', 'CTYPE1', 'CTYPE2', 'CD1_1', 'CD2_1', 'CD1_2', 'CD2_2', 'RAZP02', 'DECZP02', 'STDCRMS', 'WCSPASS']
>>> vphaslib.srctbl_keys
['Sequence_number', 'RA', 'DEC', 'X_coordinate', 'Y_coordinate', 'Peak_height', 'Peak_height_err', 'Aper_flux_3', 'Aper_flux_3_err']
>>> vphaslib.catalog_keys
['sourceID', 'RAJ2000', 'DEJ2000', 'u', 'err_u', 'g', 'err_g', 'r2', 'err_r2', 'ha', 'err_ha', 'r', 'err_r', 'i', 'err_i']
```
To see more info about the module, please call the docstring:
```python
>>> help(vphaslib)
```

## Scripts

The package contains also three ready-to-use programs in the `scripts/` directory. After installation the `vphasfits` module you can use them from anywhere. The `argparse` module is needed. More info can be found calling scripts with the `--help` option.

I encourage to visit my website to see more detailed description of this project. The current link can be found on my [GitHub profile](https://github.com/pbrus).

## License

**Vphasfits** is licensed under the [MIT license](http://opensource.org/licenses/MIT).
