import pytest
import plotme.plotme as plotme

import numpy as np
import pandas as pd


def test_plotme():
    # generate data
    df = pd.DataFrame(np.random.randn(100, 4), columns=list('ABCD'))
    df.to_csv("random_test.csv")
    # df2 = pd.read_csv("random_test.csv", index_col=0)  # for testing the test

    assert plotme.main() == 0, "should return 0"
