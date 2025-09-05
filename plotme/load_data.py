import logging
import re

from difflib import get_close_matches
from datetime import datetime
from pathlib import Path

import numpy as np

from plotme.read import read


def fuzzy_match_column(target_column, available_columns, cutoff=0.6):
    """
    Find the best fuzzy match for a target column name in available columns.
    
    Parameters:
    -----------
    target_column : str
        The column name to search for
    available_columns : list
        List of available column names in the dataframe
    cutoff : float
        Minimum similarity ratio (0.0 to 1.0)
    
    Returns:
    --------
    str or None : Best matching column name, or None if no good match found
    """
    matches = get_close_matches(target_column, available_columns, n=1,
                                cutoff=cutoff)
    if matches:
        best_match = matches[0]
        if best_match != target_column:
            logging.info(f"Fuzzy matched '{target_column}' to '{best_match}'")
        return best_match
    else:
        logging.warning(f"No close match found for '{target_column}' columns")
    return None


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


def check_filter_match(filter_value, filename):
    """
    Check if filename matches any filter criteria.
    
    Parameters:
    -----------
    filter_value : str or iterable
        Filter criteria - can be a single string or an iterable of strings
    filename : str
        The filename to check against the filter
        
    Returns:
    --------
    bool : True if any filter matches, False otherwise
    """
    if filter_value is None:
        return False
    
    # Convert string to list for uniform processing
    if isinstance(filter_value, str):
        filters = [filter_value]
    else:
        # Handle any iterable (list, tuple, set, etc.)
        try:
            filters = list(filter_value)
        except TypeError:
            # If it's not iterable, treat as single string
            filters = [str(filter_value)]
    
    # Check if any filter matches the filename
    for filter_item in filters:
        if filter_item in filename:
            return True
    
    return False


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

        self.schema = schema = args_dict.get('schema', {})
        include_filter = schema.get('file_include_filter')
        exclude_filter = schema.get('file_exclude_filter')
        header = schema.get('header', 'infer')
        x_id_in_file_name = schema.get('x_id_in_file_name', False)
        x_id_is_reg_exp = schema.get('x_id_is_reg_exp', False)
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
            for file in data_files:  # read in all the dfs
                file_path = Path(file)
                file_name = file_path.name
                if include_filter and not check_filter_match(include_filter, file_name):
                    logging.info(f"ignoring {file} because it does not match file_include_filter")
                    continue
                if exclude_filter and check_filter_match(exclude_filter, file_name):
                    logging.info(f"ignoring {file} because it matches file_exclude_filter")
                    continue
                file_info = {'file_stem' : file_path.stem,
                             'file_path': str(file_path)}
                df = read(file, index_col=index_col, header=header)
                
                # if x_id or y_id not a columns header, try to fuzzy match it
                # if matching doesn't work then skip the file
                # TODO fix before commenting in, currently breaks tests
                # if x_id not in df.columns:
                #     logging.warning(f"x_id '{x_id}' not found in {file}")
                #     # try to fuzzy match x_id
                #     x_id_fuzz = fuzzy_match_column(df.columns, x_id)
                #     if x_id_fuzz:
                #         file_info['x_id_fuzz'] = x_id_fuzz
                #     else:
                #         continue
                # TODO implement for y_id
                # can be an array so fuzzy matching is more complex
                
                # only set folder as not empty if there is plotable data
                self.empty = False
                
                if x_id_in_file_name or x_id_is_reg_exp:  # if true the df_type is point
                    file_info['x_value'] = self._retrieve_x_from_name(file)
                file_info['df_type'] = self._determine_df_type(df, file_info)
                df = preprocessing(df, self.pre)
                self.dataframes.append(df)
                self.file_infos.append(file_info)
                logging.debug(f"{file}: info: {file_info} headers: {df.columns} "
                            f"data: {df}")

            # handle folder data errors
            try:
                self._x_values()
                self._y_values()
            except Exception as e:
                logging.error(e, exc_info=True)
                logging.error(f"Above error processing folder {directory}")
                self.empty = True

        else:
            logging.debug(f"no data files found in {directory}")

    def _retrieve_x_from_name(self, filename):
        x_id = self.x_id
        x_time_format = self.schema.get('x_time_format', None)

        if self.schema.get('x_id_is_reg_exp', False):
            # x_id contains regular expression, use it to find 
            # example x_id: "_(\\d+)N"
            extracted = re.search(x_id, Path(filename).stem)
            if extracted:
                extracted = extracted.group(1)
            else:
                logging.warning(f"x_id '{x_id}' not found in filename '{filename}'")
                return None
        else:
            extracted = Path(filename).stem.split(x_id)[1].split(x_id)[0]

        if x_time_format is not None:
            time_stamp = datetime.strptime(extracted, x_time_format).timestamp()
            if self.args_dict.get('min_timestamp') is None:
                self.args_dict['min_timestamp'] = time_stamp
                x_value = 0
            else:
                x_value = time_stamp - self.args_dict['min_timestamp']
        else:
            x_value = float(extracted)
        return x_value

    def _determine_df_type(self, df, file_info):

        if isinstance(self.y_id, str):
            if self.y_id == 'headers':
                self.y_id = df.columns.to_list()
        
        if isinstance(self.y_id, list):
            n_y_ids = len(self.y_id)
        else:
            n_y_ids = 1

        if 'x_value' in file_info:
            df_type = 'point'
        else:
            if n_y_ids == 1:
                df_type = 'trace'
            elif n_y_ids > 1:
                df_type = 'plot'

        return df_type

    def _x_values(self):

        dfs = self.dataframes

        x_values = []
        for i, info in enumerate(self.file_infos):
            x_id = info.get('x_id_fuzz', self.x_id)
            x_value = info.get('x_value', None)
            if x_value is not None:
                x_values.append(x_value)
            else:
                if self.x_id == 'index':
                    values = dfs[i].index.to_list()
                else:
                    values = dfs[i][x_id].to_list()
                self.x.append({self.x_id: values})

        if len(x_values) > 0:
            self.x.append({self.x_id: x_values})

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
                        y_values.append(np.max(dfs[i][y_id]))
                    elif 'min' == post:
                        y_values.append(np.min(dfs[i][y_id]))
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
