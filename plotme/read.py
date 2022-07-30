
from pathlib import Path

import pandas as pd


def read(file_path, **kwargs):

    file_extension = Path(file_path).suffix.lower()

    if 'csv' in file_extension or 'txt' in file_extension:
        df = pd.read_csv(file_path, **kwargs)
    elif 'xls' in file_extension:
        df = pd.read_excel(file_path, **kwargs)

    return df
