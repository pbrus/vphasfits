#!/usr/bin/env python3

from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from textwrap import dedent

from vphasfits import convert_src_table_fits_to_txt


arg_parser = ArgumentParser(
    prog=f"{Path(__file__).name}",
    description="Convert source table FITS from VPHAS+ project to a text file",
    epilog="Copyright (c) https://github.com/pbrus",
    formatter_class=RawTextHelpFormatter,
)

arg_parser.add_argument(
    "table",
    help=dedent(
        """\
    source table in FITS format
    """
    ),
    type=str,
    metavar="filename",
)

arg_parser.add_argument(
    "pawprint",
    help=dedent(
        """\
    a number pointing a proper pawprint
    of the mosaic (from 1 to 32)
    """
    ),
    metavar="pawprint",
    type=int,
    choices=range(1, 33),
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
convert_src_table_fits_to_txt(args.table, args.pawprint, args.output)
