import glob

from pathlib import Path

import numpy as np
import pandas as pd


def collect_1_x_per_file(directory, param_id, column_id, split_on='_'):
    match_string = str(Path(directory, "*.xlsx"))
    xlsx_files = glob.glob(match_string, recursive=False)
    y_values = []
    x_values = []
    for file in xlsx_files:
        # TODO use regular expressions instead to find the x from a file name
        param_value = Path(file).stem.split(param_id)[1].split(split_on)[0]
        param_value = float(param_value)
        x_values.append(param_value)
        df = pd.read_excel(file, engine='openpyxl')
        #df = pre_process_abs_sum_remove(df, to_remove=0., col_1='', col_2='')  # get variables from plot_info
        try:
            max_norm_cont = max(df[column_id])
        except ValueError:
            max_norm_cont = 0
        y_values.append(max_norm_cont)

    return x_values, y_values


# this function should take plot_info and live in a different file or this python file should be changed
# to be non-file type specific
def pre_process_abs_sum_remove(df, to_remove=0., col_1='', col_2=''):

    two_col_abs_then_summed_by_row = np.absolute(df[col_1]) + np.absolute(df[col_2])
    idxs = np.where(two_col_abs_then_summed_by_row == to_remove)[0]
    df = df.drop(labels=idxs, axis=0)

    return df