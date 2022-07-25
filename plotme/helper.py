""" Copyright (c) 3M, 2020. All rights reserved.
helper.py contains data related helper functions including import,
verification, manipulation, logging, and upload used by roadrunner.py
"""
import collections.abc
import datetime as dt
import importlib
import logging
import os
from pathlib import Path


def start_logging(log_folder='', log_level=logging.INFO, file_name='',
                  date_time_stamp=''):
    """
    Sets up the log file using python's built in logging
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

    logging.debug('debug logging active')
    logging.info('info logging active')
    logging.warning('warning logging active')
    logging.error('error logging active')


def deep_update(to_update, update):
    """
    Update a nested dictionary or similar mapping.
    Modifies ``source`` in place.
    Parameters
    ----------
    to_update: dict
        dictionary to update in place
    update: dict
        new items for dict
    Returns
    -------
    to_update: dict
        dictionary with updated values, needed for recursion?
    """
    for k, v in update.items():
        if isinstance(v, collections.abc.Mapping):
            to_update[k] = deep_update(to_update.get(k, {}), v)
        else:
            to_update[k] = v
    return to_update


def try_for(func, args=[], iterations=3):
    """
    for loop with try and error handling around any method
    Parameters
    ----------
    func: method
        function
    iterations: int
        number of iterations to run
    args: tuple
        arguments
    Returns
    -------
    output: list
        output objects or variables
    """

    success = False
    for x in range(1, iterations + 1):
        try:
            output = func(*args)
            success = True
            break
        except Exception as e:
            logging.error(e, exc_info=True)
            logging.warning(f'try_for: exception during attempt {x}, trying '
                            f'{func.__name__}() again')

    if success is False:
        raise Exception(f"try_for: final attempt to execute {func.__name__}()"
                        " failed, exiting")

    return output

