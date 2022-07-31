import argparse
import logging
import sys

import helper
from plotme import __version__
from plotme.plotting import plot_all

# parse the arguments
parser = argparse.ArgumentParser(description='automates plotting of tabular data')

parser.add_argument('-s', dest='data_root', action="store", default="", type=str,
                    help="Specify data directory")
parser.add_argument('-gt', dest='template', action="store_true",
                    help="generate a template")
parser.add_argument('-f', dest='force', action="store_true",
                    help="force regeneration of all plots")
parser.add_argument('-v', dest='report_version', action="store_true",
                    help="report the version of plotme")

args_dict = vars(parser.parse_args())

if args_dict['report_version']:
    print(f"plotme version: {__version__}")
    sys.exit(0)

helper.start_logging(log_level=logging.INFO)

try:
    plot_all(args_dict)
except Exception as e:
    logging.exception("Fatal error in main")
    logging.error(e, exc_info=True)
    sys.exit(1)
