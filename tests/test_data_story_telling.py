'''
Author: Ariel da Silva Alsina
Date: 26/11/2021
test file for the pytest.
'''
from logging import root
import os
import pandas as pd
from pathlib import Path, PurePath
from data_story_telling import read_file, format_columns, get_rolling_window



root_path = Path(__file__)
root_path = root_path.parent.absolute().parent
data_path = Path('data/euro-daily-hist_1999_2021.csv')
path = PurePath(root_path, data_path)

def test_read_file():
    exchange_rates = read_file(path)
    assert isinstance(exchange_rates, pd.DataFrame) is True

def test_get_rolling_window():
    exchange_rates = read_file(path)

    # renaming the column names
    replace_map = {
        '[': '',
        ' ]': '',
        ' ': '_'
    }
    format_columns(exchange_rates, replace_map)
    exchange_rates = exchange_rates[exchange_rates['US_dollar'] != '-']
    assert isinstance(get_rolling_window(exchange_rates['US_dollar'], 15), pd.Series) is True
