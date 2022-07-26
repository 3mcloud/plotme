import glob

from pathlib import Path

import numpy as np
import pandas as pd

from read import read


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
        df = build_data("xlsx", file)
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


def load(directory, x_id='', y_id='', kwargs={}):
    schema = kwargs.get('schema', {})
    file_extension = schema.get('file_extension', 'csv')
    match_string = str(Path(directory, f"*.{file_extension}"))
    data_files = glob.glob(match_string, recursive=False)
    y_values = []
    x_values = []
    if len(data_files) == 1:  # assume data file contains at least 1 trace
        df = read(data_files[0], index_col=0)
    else:
        for file in data_files:
            if isinstance(y_id, str):
                x_value = Path(file).stem.split(x_id)[1].split(x_id)[0]
                x_value = float(x_value)
                x_values.append(x_value)
                df = build_data("xlsx", file)
                try:
                    y_value = max(df[y_id])
                except ValueError:
                    y_value = 0
                y_values.append(y_value)
            # elif isinstance(y_id, list):

    return df


def build_data(dtype, d_path) -> pd.DataFrame:
    if dtype == "xlsx":
        cl = from_xlsx(d_path)
        df = cl.retrieve_data()
    elif dtype == "csv":
        return
    else:
        print("Unrecognized data file type")
        exit(1)
    return df


class Data:
    def __init__(self) -> None:
        super(Data, self).__init__()
    
    def retrieve_data(self):
        return self([])
    #Open file
    #Retrieve x
    #Retrieve y
    #Preprocessing
    #Postprocessing
    #Return refined data


class from_xlsx(Data):
    def __init__(self, d_path) -> None:
        super(from_xlsx, self).__init__()
        self.d_path = d_path


    def call(self, input, **kwargs):
        df = pd.read_excel(self.d_path, engine='openpyxl')
        return df