#!/usr/bin/env python3

from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from textwrap import dedent

from vphasfits import convert_catalog_fits_to_txt


arg_parser = ArgumentParser(
    prog=f"{Path(__file__).name}",
    description="Convert catalog FITS from VPHAS+ project to a text file",
    epilog="Copyright (c) https://github.com/pbrus",
    formatter_class=RawTextHelpFormatter,
)

arg_parser.add_argument(
    "catalog",
    help=dedent(
        """\
    catalog in FITS format
    """
    ),
    type=str,
    metavar="filename",
)

arg_parser.add_argument(
    "--output",
    help=dedent(
        """\
    name of the output file
    """
    ),
    metavar="filename",
    type=str,
    default=None,
)

args = arg_parser.parse_args()
convert_catalog_fits_to_txt(args.catalog, args.output)
