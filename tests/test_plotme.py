import json
import os

import pytest
import numpy as np
import pandas as pd

from plotme.plotting import plot_all
from plotme.plotting import template_file_name


def test_plotme():
    # generate data
    df = pd.DataFrame(np.random.randn(100, 4), columns=list('ABCD'))
    df.to_csv("random_test.csv")
    # df2 = pd.read_csv("random_test.csv", index_col=0)  # for testing the test
    test_plot_info = {"title_text": "test plot"}
    test_plot_info_stream = json.dumps(test_plot_info, sort_keys=False, indent=4)
    test_spec_file = "test_plot_info.json"
    with open(test_spec_file, "w") as json_file:
        json_file.write(test_plot_info_stream)

    ret = plot_all({"force": True})

    # os.remove(test_spec_file)

    assert ret == 0, "should return 0"


def test_template_gen():
    # generate data

    ret = plot_all({"template": True})

    os.remove(template_file_name)

    assert ret == 0, "should return 0"

