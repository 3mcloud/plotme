
from pathlib import Path

import pandas as pd


def read(file_path, **kwargs):

    file_extension = Path(file_path).suffix.lower()

    if file_extension == 'csv':
        df = pd.read_csv(file_path, **kwargs)
