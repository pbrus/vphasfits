#!/usr/bin/env python3

from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from textwrap import dedent

from vphasfits import pawprint_from_mef


arg_parser = ArgumentParser(
    prog=f"{Path(__file__).name}",
    description="Get a pawprint from MEF image (VPHAS+)",
    epilog="Copyright (c) https://github.com/pbrus",
    formatter_class=RawTextHelpFormatter,
)

arg_parser.add_argument(
    "image",
    help=dedent(
        """\
    FITS mosaic (MEF)
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
pawprint_from_mef(args.image, args.pawprint, args.output)
