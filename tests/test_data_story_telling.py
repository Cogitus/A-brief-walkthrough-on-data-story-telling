'''
Author: Ariel da Silva Alsina
Date: 26/11/2021
test file for the pytest.
'''
import pandas as pd
from data_story_telling import read_file, format_columns, get_rolling_window


def test_read_file():
    read_file(r'data/euro-daily-hist_1999_202.csv')

def test_format_columns():
    exchange_rates = read_file(r'./data/euro-daily-hist_1999_202.csv')
    # renaming the column names
    replace_map = {
        '[': '',
        ' ]': '',
        ' ': '_'
    }
    format_columns(exchange_rates, replace_map)

    assert type(format_columns) == pd.Series

def test_get_rolling_window():
    exchange_rates = read_file(r'data/euro-daily-hist_1999_202.csv')

    # renaming the column names
    replace_map = {
        '[': '',
        ' ]': '',
        ' ': '_'
    }
    format_columns(exchange_rates, replace_map)
    exchange_rates = [exchange_rates['US_dollar'] != '-']
    assert type(exchange_rates['US_dollar'].rolling(15).mean()) == Series
   

if __name__ == '__main__':
    exchange_rates = read_file(r'./data/euro-daily-hist_1999_202.csv')
    # renaming the column names
    replace_map = {
        '[': '',
        ' ]': '',
        ' ': '_'
    }
    format_columns(exchange_rates, replace_map)

    assert type(format_columns) == pd.Series