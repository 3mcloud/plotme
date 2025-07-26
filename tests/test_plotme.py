import json
import os

import pytest
import numpy as np
import pandas as pd

from plotme.plotting import plot_all
from plotme.plotting import template_file_name

def init_test():
    # start_logging(log_level=logging.DEBUG)
    try:
        os.chdir("tests")
    except: 
        pass
    

def test_simple_random_data():
    init_test()
    # generate data
    df = pd.DataFrame(np.random.randn(100, 4), columns=list('ABCD'))
    data_file_name = "random_test.csv"
    df.to_csv(data_file_name)
    # df2 = pd.read_csv("random_test.csv", index_col=0)  # for testing the test
    test_plot_info = {
        "title_text": "simple random data",
        "schema": {
            "include_filter": data_file_name,
        },
    }
    test_plot_info_stream = json.dumps(test_plot_info, sort_keys=False, indent=4)
    plot_info_filter = "simple_random_data"
    test_spec_file = f"{plot_info_filter}.json"
    with open(test_spec_file, "w") as json_file:
        json_file.write(test_plot_info_stream)

    ret = plot_all({"force": True, "plot_info_file": plot_info_filter})

    os.remove(test_spec_file)

    assert ret == 0, "should return 0"


def test_template_gen():
    init_test()
    # generate data

    ret = plot_all({"template": True})

    os.remove(template_file_name)

    assert ret == 0, "should return 0"


def test_housing_data():
    init_test()

    data_root = "housing"
    ret = plot_all({"force": True, "data_root": data_root})

    assert ret == 0, "should return 0"

def test_local_data():

    os.chdir(r"D:\localData")

    ret = plot_all({"force": True})

    assert ret == 0, "should return 0"