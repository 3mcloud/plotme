import glob
import logging

from pathlib import Path

import numpy as np
import pandas as pd

from read import read


# def collect_1_x_per_file(directory, param_id, column_id, split_on='_'):
#     match_string = str(Path(directory, "*.xlsx"))
#     xlsx_files = glob.glob(match_string, recursive=False)
#     y_values = []
#     x_values = []
#     for file in xlsx_files:
#         # TODO use regular expressions instead to find the x from a file name
#         param_value = Path(file).stem.split(param_id)[1].split(split_on)[0]
#         param_value = float(param_value)
#         x_values.append(param_value)
#         df = build_data("xlsx", file)
#         #df = pre_process_abs_sum_remove(df, to_remove=0., col_1='', col_2='')  # get variables from plot_info
#         try:
#             max_norm_cont = max(df[column_id])
#         except ValueError:
#             max_norm_cont = 0
#         y_values.append(max_norm_cont)
#
#     return x_values, y_values


# this function should take plot_info and live in a different file or this python file should be changed
# to be non-file type specific
def pre_process_abs_sum_remove(df, to_remove=0., col_1='', col_2=''):
    two_col_abs_then_summed_by_row = np.absolute(df[col_1]) + np.absolute(df[col_2])
    idxs = np.where(two_col_abs_then_summed_by_row == to_remove)[0]
    df = df.drop(labels=idxs, axis=0)

    return df


def preprocessing(df, pre):
    return_df = df
    for conditions in pre:
        if conditions["remove_null"] == "all":
            return_df = df.dropna()
        if conditions["remove_zero"] == "all":
            return_df = df.loc[(df!=0).all(axis=1)]
    return return_df



# def retrieve_x(filename, x_id, df, x_values, kwargs={}):
#     name_significance = kwargs.get('name_significance', "None")
#     # appends list for filename significance
#     if name_significance == "x_values":
#         x = retrieve_x_from_name(filename, x_id)
#         x_values.append(x)
#     # returns x_values if x_values already populated
#     elif x_values.size is not 0:
#         x = x_values
#     # finds x_values if none exist
#     else:
#         x = df[x_id]
#     return x


def retrieve_x_from_name(filename, x_id):
    x_value = Path(filename).stem.split(x_id)[1].split(x_id)[0]
    x_value = float(x_value)
    return x_value


class Folder(object):
    def __init__(self, directory, x_id='', y_id='', kwargs={}):

        self.kwargs = kwargs
        self.x_id = x_id
        self.y_id = y_id
        self.pre = kwargs.get('pre', {})
        self.post = kwargs.get('post', {})

        self.x = []  # list of dicts
        self.y = []  # list of dicts

        schema = kwargs.get('schema', {})
        x_id_in_file_name = schema.get('x_id_in_file_name', False)
        index_col = schema.get('index_col')
        file_extensions = schema.get('file_extension', ['csv', 'xlsx', 'xls'])
        if isinstance(file_extensions, str):
            file_extensions = [file_extensions]
        data_files = []
        for file_extension in file_extensions:
            match_string = str(Path(directory, f"*.{file_extension}"))
            data_files.extend(glob.glob(match_string, recursive=False))
        self.dataframes = []
        self.file_infos = []
        if len(data_files) == 0:
            logging.debug(f"no data files found in {directory}")
            return None
        elif len(data_files) > 0:
            for file in data_files:  # read in all the dfs
                file_info = {}
                df = read(file, index_col=index_col)
                if x_id_in_file_name:  # if true this also means the df is for a single point!
                    file_info['x_value'] = retrieve_x_from_name(file, x_id)
                file_info['df_type'] = self.determine_df_type(df, file_info)
                df = preprocessing(df, self.pre)
                self.dataframes.append(df)
                self.file_infos.append(file_info)

                # else:
        #     x_values = []
        #     for file in data_files:
        #         if isinstance(y_id, str):
        #             df = build_data("xlsx", file)
        #             x_values = retrieve_x(file, x_id, df, x_values, kwargs)

        # if isinstance(y_id, str):
        #     x_value = Path(file).stem.split(x_id)[1].split(x_id)[0]
        #     x_value = float(x_value)
        #     x_values.append(x_value)
        #     df = read(data_files[0], index_col=0)
        #     try:
        #         y_value = max(df[y_id])
        #     except ValueError:
        #         y_value = 0
        #     y_values.append(y_value)
        # # elif isinstance(y_id, list):

    def determine_df_type(self, df, file_info):

        y_id = self.y_id
        if isinstance(y_id, str):
            if y_id == 'headers':
                self.y_id = df.columns.to_list()

        n_y_ids = len(self.y_id)

        if file_info.get('x_value'):
            df_type = 'point'
        else:
            if n_y_ids == 1:
                df_type = 'trace'
            elif n_y_ids > 1:
                df_type = 'plot'

        return df_type

    def x_values(self):

        x_id = self.x_id
        dfs = self.dataframes

        x_values = []
        for i, info in enumerate(self.file_infos):
            x_value = info.get('x_value')
            if x_value:
                x_values.append(x_value)
            else:
                if x_id == 'index':
                    values = dfs[i].index.to_list()
                else:
                    values = dfs[i][x_id].to_list()
                self.x.append({x_id: values})

        if len(x_values) > 0:
            self.x.append({x_id:x_values})

        return self.x

    def y_values(self):

        y_id = self.y_id
        post = self.post
        post_keys = post.keys()
        dfs = self.dataframes

        if isinstance(y_id, str):
            y_ids = [y_id]
        elif isinstance(y_id, list):
            y_ids = y_id
        else:
            logging.error("y_id problem")

        y_values = []

        for i, info in enumerate(self.file_infos):

            if info['df_type'] == 'point':
                for y_id in y_ids:
                    # TODO implement more post process
                    if 'avg' in post_keys:
                        y_values.append(np.average(dfs[i][y_id]))
                    else:
                        y_values.append(dfs[i][y_id][0])  # take the 1st value in the column
            else:
                traces = []
                for y_id in y_ids:
                    points = dfs[i][y_id].to_list()
                    traces.append({y_id: points})
                self.y.append(traces)

        if len(y_values) > 0:
            self.y.append([{y_id: y_values}])

        return self.y
    
    



# def build_data(dtype, d_path) -> pd.DataFrame:
#     if dtype == "xlsx":
#         cl = from_xlsx(d_path)
#         df = cl.retrieve_data()
#     elif dtype == "csv":
#         return
#     else:
#         print("Unrecognized data file type")
#         exit(1)
#     return df


# class Data(object):
#     def __init__(self) -> None:
#         # super(Data, self).__init__()
#
#
#     def retrieve_data(self):
#         return self([])
#     #Open file
#     #Retrieve x
#     #Retrieve y
#     #Preprocessing
#     #Postprocessing
#     #Return refined data
#
#
# class from_xlsx(Data):
#     def __init__(self, d_path) -> None:
#         super(from_xlsx, self).__init__()
#         self.d_path = d_path
#
#
#     def call(self, input, **kwargs):
#         df = pd.read_excel(self.d_path, engine='openpyxl')
#         return df
#
#
# class Trace(object):
#     def __init__(self) -> None:
#
# class Plot(object):
#     def __init__(self) -> None:
