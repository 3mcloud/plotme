import glob
import logging

from pathlib import Path

import numpy as np

from plotme.read import read


# this function should take plot_info and live in a different file or this python file should be changed
# to be non-file type specific
def pre_process_abs_sum_remove(df, to_remove=0., col_1='', col_2=''):
    two_col_abs_then_summed_by_row = np.absolute(df[col_1]) + np.absolute(df[col_2])
    idxs = np.where(two_col_abs_then_summed_by_row == to_remove)[0]
    df = df.drop(labels=idxs, axis=0)

    return df


def preprocessing(df, pre):
    # use loop to sequence pre-processing steps
    for step in pre:
        match step:
            case "remove_null":
                df = df.dropna()
            case "remove_zero":
                df = df.loc[(df!=0).all(axis=1)]
            case "remove_strings":
                # Remove rows containing any string value
                df = df.loc[df.map(lambda x: not isinstance(x, str)).all(axis=1)]
            case "convert_to_float":
                # Convert all cells in dataframe to float
                df = df.astype(float)
            case _:  # Default case (optional)
                logging.warning(f"Unknown preprocessing step: {step}")
    return df


def retrieve_x_from_name(filename, x_id):
    x_value = Path(filename).stem.split(x_id)[1].split(x_id)[0]
    x_value = float(x_value)
    return x_value


class Folder(object):
    def __init__(self, directory, x_id='', y_id='', args_dict={}):

        self.args_dict = args_dict
        self.x_id = x_id
        self.y_id = y_id
        self.pre = args_dict.get('pre', [])
        self.post = args_dict.get('post')
        self.name = Path(directory).name

        self.x = []  # list of dicts
        self.y = []  # list of dicts

        self.empty = True

        schema = args_dict.get('schema', {})
        header = schema.get('header', 'infer')
        x_id_in_file_name = schema.get('x_id_in_file_name', False)
        index_col = schema.get('index_col')
        file_extensions = schema.get('file_extension', ['csv', 'xlsx', 'xls'])
        if isinstance(file_extensions, str):
            file_extensions = [file_extensions]
        data_files = []
        for file_extension in file_extensions:
            # TODO rename file_extension or split into 2 variables
            match_string = str(Path(f"*{file_extension}"))
            ext_data = list(Path(directory).glob(match_string))
            data_files.extend(ext_data)
            logging.debug(f"{directory}'s match_string: {match_string}")
        logging.debug(f"{directory}'s data_files: {data_files}")
        self.dataframes = []
        self.file_infos = []
        if len(data_files) > 0:
            self.empty = False
            for file in data_files:  # read in all the dfs
                file_name = Path(file).stem
                file_info = {'file_name' : file_name}
                df = read(file, index_col=index_col, header=header)
                if x_id_in_file_name:  # if true this also means the df is for a single point!
                    file_info['x_value'] = retrieve_x_from_name(file, x_id)
                file_info['df_type'] = self.determine_df_type(df, file_info)
                df = preprocessing(df, self.pre)
                self.dataframes.append(df)
                self.file_infos.append(file_info)
                logging.debug(f"{file}: info: {file_info} headers: {df.columns} "
                            f"data: {df}")

            self._x_values()
            self._y_values()

        else:
            logging.debug(f"no data files found in {directory}")

    def determine_df_type(self, df, file_info):

        if isinstance(self.y_id, str):
            if self.y_id == 'headers':
                self.y_id = df.columns.to_list()
        
        if isinstance(self.y_id, list):
            n_y_ids = len(self.y_id)
        else:
            n_y_ids = 1

        if file_info.get('x_value'):
            df_type = 'point'
        else:
            if n_y_ids == 1:
                df_type = 'trace'
            elif n_y_ids > 1:
                df_type = 'plot'

        return df_type

    def _x_values(self):

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

    def _y_values(self):

        y_id = self.y_id
        post = self.post
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
                    if 'avg' == post:
                        y_values.append(np.average(dfs[i][y_id]))
                    elif 'max' == post:
                        y_values.append(np.maximum(dfs[i][y_id]))
                    elif 'min' == post:
                        y_values.append(np.minimum(dfs[i][y_id]))
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
