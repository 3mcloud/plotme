import argparse
import logging
import sys

from plotme import helper
from plotme import __version__
from plotme.plotting import plot_all
from plotme.plotting import plot_info_id

def run():
    # parse the arguments
    parser = argparse.ArgumentParser(
        description='automates plotting of tabular data, all arguments are optional')

    parser.add_argument('--json', dest='plot_info_file', action="store",
                        default=plot_info_id, type=str,
                        help="String to find config, default 'plot_info'")
    parser.add_argument('-d', dest='data_root', action="store", default="",
                        type=str, help="Search directory, defaults to current")
    parser.add_argument('-gt', dest='template', action="store_true",
                        help="generate a plot_info template")
    parser.add_argument('-f', dest='force', action="store_true",
                        help="force regeneration of all plots")
    parser.add_argument('-v', dest='report_version', action="store_true",
                        help="report the version of plotme")
    parser.add_argument('--no-html', dest='html', action="store_false",
                        help="save .html file of each plot")
    parser.add_argument('--png', dest='png', action="store_true",
                        help="save .png file of each plot")
    parser.add_argument('--quiet', dest='show', action="store_false",
                        help="don't open each plot in a browser tab")
    parser.add_argument('--debug', dest='debug', action="store_true",
                        help="enable debug logging")

    args_dict = vars(parser.parse_args())

    version_info = f"plotme version: {__version__}"
    if args_dict['report_version']:
        print(version_info)
        sys.exit(0)

    if args_dict["debug"]:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    helper.start_logging(log_level=log_level, log_level_test=args_dict["debug"])
    logging.info(version_info)

    try:
        plot_all(args_dict)
    except Exception as e:
        logging.exception("Fatal error in main")
        logging.error(e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":

    run()
