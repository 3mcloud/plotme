"""
helper.py contains helper functions
"""
import datetime as dt
import importlib
import logging
import os
from pathlib import Path


def start_logging(log_folder='', log_level=logging.INFO, file_name='',
                  date_time_stamp='', log_level_test=True):
    """
    Sets up the log file using python's built in logging.

    Parameters
    ----------
    log_folder: str
        relative path to experiment folder
    log_level: int
        integer representing logging severity level
    file_name: str
        experiment name
    date_time_stamp: str
        date + time stamp
    log_level_test: bool
        enable/disable the log level test
    """

    # in case it is already running shutdown the logging library and reload it
    # basicConfig only works the 1st time it's called unless you do this
    logging.shutdown()
    importlib.reload(logging)

    if len(date_time_stamp) == 0:
        date_time_stamp = dt.datetime.now().strftime('%Y%m%d_%H.%M.%S')
    if len(log_folder) > 1:
        file_name = os.path.join(log_folder, f"{date_time_stamp}_{file_name}.log")
        Path(file_name).parent.mkdir(parents=True, exist_ok=True)
    else:
        file_name = 'log.log'
    logging_format = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(filename=file_name, level=log_level, format=logging_format)

    # Get the top-level logger object
    log = logging.getLogger()
    # make the log print to the console.
    console = logging.StreamHandler()
    log.addHandler(console)

    if log_level_test:
        logging.debug('debug logging active')
        logging.info('info logging active')
        logging.warning('warning logging active')
        logging.error('error logging active')
