'''
    Autor: Ariel da Silva Alsina
    Date: 26/10/2021
'''
import logging

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style



# setup of the logging
logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def read_file(path):
    '''
    Reads the data's .csv and returns the dataframe

    Args:
        path (str): path of the .csv;
    Return:
        exchange_df (DateFrame): table of the exchange rates;
    '''
    # reading the data
    try:
        exchange_df = pd.read_csv(path)
        return exchange_df
    except FileNotFoundError:
        logging.error('File not readed.')
        return None


def format_columns(df2format, format_dict):
    '''
    Replace the specified characters of the DataFrame's columns. Note the dict keys orders
    its relevant.

    Args:
        df2format (DataFrame): the dataframe that is going to be filtered;
        format_dict (dict): the dict of characters to be removed;
    Return:
        None;
    '''
    for character, to_replace in format_dict.items():
        df2format.columns = [column.replace(character, to_replace)
                            for column in df2format.columns]

def get_rolling_window(data_series, window_size):
    '''
    Get a rolling window of size 'window_size' from a Series;

    Args:
        data_series (Series): the data which the rolling window will be extracted;
        window_size (int): the rolling window size;
    Return:

    '''
    return data_series.rolling(window_size).mean()

if __name__ == '__main__':
    exchange_rates = read_file(r'data/euro-daily-hist_1999_202.csv')

    # renaming the column names
    replace_map = {
        '[': '',
        ' ]': '',
        ' ': '_'
    }
    format_columns(exchange_rates, replace_map)

    exchange_rates.rename(columns={r'Period\Unit:': 'Time'}, inplace=True)

    # changing the type of the Time column to datetime
    exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])

    # sorting the dates
    exchange_rates.sort_values('Time', ascending=True, inplace=True)

    # reseting the index and droping it
    exchange_rates.reset_index(drop=True, inplace=True)

    # segmenting the dataset for the dollar
    euro2dollar = exchange_rates[['Time', 'US_dollar']].copy()  # pylint: disable = E1136
    # segmenting the dataset for the real
    euro2real = exchange_rates[['Time', 'Brazilian_real']].copy()   # pylint: disable = E1136

    # filtering for the non '-' values on both dataframes
    euro2dollar = euro2dollar[euro2dollar['US_dollar'] != '-']
    euro2real = euro2real[euro2real['Brazilian_real'] != '-']


    # the temporary plotting style
    style.use('seaborn-talk')
    fig, (AX1, AX2) = plt.subplots(1, 2, figsize=(15, 6))

    AX1.plot(euro2dollar['Time'], euro2dollar['US_dollar'])
    AX2.plot(euro2real['Time'], euro2real['Brazilian_real'])

    for AX in [AX1, AX2]:
        AX.set_xlabel('Year')
        AX.set_ylabel('Coin Value')

        for location in ['right', 'top']:
            AX.spines[location].set_visible(False)

    AX1.set_title('Evolution of the Euro-Dollar Exchange Rate', size=20, weight='bold')
    AX2.set_title('Evolution of the Euro-Real Exchange Rate', size=20, weight='bold')

    plt.show()


    fig = plt.figure(figsize=(12, 15))

    rolling_window = [1, 7, 30, 50, 100, 365]
    plot_number = range(1, 7)
    for i, rolling_mean in zip(plot_number, rolling_window):
        AX = fig.add_subplot(3, 2, i)

        for location in ['right', 'top']:
            AX.spines[location].set_visible(False)

        plt.title('Rolling Window:' + str(rolling_mean), weight='bold')
        AX.plot(euro2dollar['Time'], euro2dollar['US_dollar'].rolling(rolling_mean).mean(),
                color='lightblue', label='dollar', alpha=0.8)
        AX.plot(euro2real['Time'], euro2real['Brazilian_real'].rolling(rolling_mean).mean(),
                color='red', label='Real')
        AX.legend()

    plt.tight_layout()
    plt.show()

    # setting the rollng mean for euro2real and euro2dollar
    euro2dollar['rolling_mean'] = get_rolling_window(euro2dollar['US_dollar'], 30)
    euro2real['rolling_mean'] = get_rolling_window(euro2real['Brazilian_real'], 30)


    # segmenting the full dataset to its respective president
    df_all_presidents = euro2dollar.copy().loc[(euro2dollar['Time'].dt.year >= 2001)]
    bush = df_all_presidents.copy().loc[df_all_presidents['Time'].dt.year < 2009]
    obama = df_all_presidents.copy().loc[(euro2dollar['Time'].dt.year >= 2009)
                                        & (euro2dollar['Time'].dt.year < 2017)]
    trump = df_all_presidents.copy().loc[(df_all_presidents['Time'].dt.year >= 2017)
                                        & (df_all_presidents['Time'] < '2021-01-20')]
    biden = df_all_presidents.copy().loc[(df_all_presidents['Time'] >= '2021-01-20')]

    style.use('fivethirtyeight')

    # creating the subplots
    plt.figure(figsize=(20, 10))

    # two rows: one with 3 graphs side-to-side and the second with only a bigger graph
    AX1 = plt.subplot(2, 4, 1)
    AX2 = plt.subplot(2, 4, 2)
    AX3 = plt.subplot(2, 4, 3)
    AX4 = plt.subplot(2, 4, 4)
    AX5 = plt.subplot(2, 1, 2)

    # changes to all the subplots
    axes_list = [AX1, AX2, AX3, AX4, AX5]
    for AX in axes_list:
        AX.set_ylim(0.8, 1.7)
        AX.set_yticks([1.0, 1.2, 1.4, 1.6])
        AX.set_yticklabels(['1.0', '1.2','1.4', '1.6'],  alpha=0.3)
        AX.grid(alpha=0.5)

    # ploting for Bush
    AX1.plot(bush['Time'], bush['rolling_mean'], color='#00BFAF')
    AX1.set_xticklabels(['', '2001', '', '2003', '', '2005', '', '2007', '', '2009'], alpha=0.3)
    AX1.text(12500, 1.85, 'BUSH', fontsize=18, weight='bold', color='#00FFAF')
    AX1.text(12330, 1.8, '(2001-2009)', weight='bold', alpha=0.3)

    # plotting for Obama
    AX2.plot(obama['Time'], obama['rolling_mean'], color='#00BFFF')
    AX2.set_xticklabels(['', '2009', '', '2011', '', '2013', '', '2015', '', '2017'], alpha=0.3)
    AX2.text(15300.0, 1.85, 'OBAMA', fontsize=18, weight='bold', color='#00BFFF')
    AX2.text(15200.0, 1.8, '(2009-2017)', weight='bold', alpha=0.3)

    # plotting for Trump
    AX3.plot(trump['Time'], trump['rolling_mean'], color='#4B7FFF')
    AX3.set_xticklabels(['2017', '', '2018', '', '2019', '', '2020', '', '2021'], alpha=0.3)
    AX3.text(17700.0, 1.85, 'TRUMP', fontsize=18, weight='bold', color='#4B7FFF')
    AX3.text(17640.0, 1.8, '(2017-2021)', weight='bold', alpha=0.3)

    #plotting for Biden
    AX4.plot(biden['Time'], biden['rolling_mean'], color='#FF0000')
    AX4.set_xticklabels(['2021', '', '2022'], alpha=0.3)
    AX4.text(18740.0, 1.85, 'BIDEN', fontsize=18, weight='bold', color='#FF0000')
    AX4.text(18725.0, 1.8, '(2017-2021)', weight='bold', alpha=0.3)

    # plotting for all presidents together
    AX5.plot(bush['Time'], bush['rolling_mean'], color='#00BFAF')
    AX5.plot(obama['Time'], obama['rolling_mean'], color='#00BFFF')
    AX5.plot(trump['Time'], trump['rolling_mean'], color='#4B7FFF')

    AX5.plot(bush['Time'], bush['rolling_mean'], color='#00BFAF')
    AX5.plot(obama['Time'], obama['rolling_mean'], color='#00BFFF')
    AX5.plot(trump['Time'], trump['rolling_mean'], color='#4B7FFF')
    AX5.plot(biden['Time'], biden['rolling_mean'], color='#FF0000')
    AX5.grid(alpha=0.5)
    AX5.set_xticks([])

    # title and subtile being added
    AX1.text(13000.0, 2.12, 'EURO-USD rate averaged 1.22 under the last three US presidents',
            fontsize=22, weight='bold')
    AX1.text(13000.0, 2.0, '''EURO-USD exchange rates under George W. Bush (2001 - 2009),
            Barack Obama (2009-2017), and Donald Trump (2017-2021)''', fontsize=16)

    # adding the signature
    AX5.text(10500.0, 0.65, '©Ariel Alsina' + ' '*230 + 'Source: European Central Bank',
            color='#f0f0f0', backgroundcolor='#4d4d4d',
            size=14)

    plt.show()


    df_all_brazil = euro2real.copy()
    fhc = df_all_brazil.copy()[df_all_brazil['Time'].dt.year < 2002]
    lula = df_all_brazil.copy()[(df_all_brazil['Time'].dt.year >= 2002)
                                & (df_all_brazil['Time'].dt.year < 2010)]
    dilma = df_all_brazil.copy()[(df_all_brazil['Time'].dt.year >= 2010)
                                & (df_all_brazil['Time'] < '2016-09-01')]
    temer = df_all_brazil.copy()[(df_all_brazil['Time'] >= '2016-09-01')
                                & (df_all_brazil['Time'].dt.year < 2018)]
    bozo = df_all_brazil.copy()[(df_all_brazil['Time'].dt.year >= 2018)]

    style.use('fivethirtyeight')
    # creating the subplots
    plt.figure(figsize=(20, 10))

    # two rows: one with 3 graphs side-to-side and the second with only a bigger graph
    AX_FHC = plt.subplot(2, 5, 1)
    AX_LULA = plt.subplot(2, 5, 2)
    AX_DILMA = plt.subplot(2, 5, 3)
    AX_TEMER = plt.subplot(2, 5, 4)
    AX_BOZO = plt.subplot(2, 5, 5)
    AX_ALL = plt.subplot(2, 1, 2)

    # changes to all the subplots
    axes = [AX_FHC, AX_LULA, AX_DILMA, AX_TEMER, AX_BOZO, AX_ALL]
    for ax in axes:
        ax.set_ylim(0.8, 1.7)
        ax.set_yticks([1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0])
        ax.set_yticklabels(['1.5', '2','2.5', '3', '3.5', '4',
                            '4.5', '5', '5.5', '6', '6.5', '7.0'], alpha=0.3)
        ax.grid(alpha=0.5)

    # ploting for FHC
    AX_FHC.plot(fhc['Time'], fhc['rolling_mean'], color='#571845')
    AX_FHC.set_xticklabels(['1999', '', '', '2001', '', '', '2002'], alpha=0.3)
    AX_FHC.text(11300.0, 7.7, 'FHC', fontsize=18, weight='bold', color='#571845')
    AX_FHC.text(11200, 7.4, '(1999-2002)', weight='bold', alpha=0.3)

    # plotting for Lula
    AX_LULA.plot(lula['Time'], lula['rolling_mean'], color='#900C3E')
    AX_LULA.set_xticklabels(['', '2003', '', '', '', '2007', '', '', '', '2011'], alpha=0.3)
    AX_LULA.text(12700.0, 7.7, 'LULA', fontsize=18, weight='bold', color='#900C3E')
    AX_LULA.text(12430.0, 7.4, '(2002-2010)', weight='bold', alpha=0.3)

    # plotting for Dilma
    AX_DILMA.plot(dilma['Time'], dilma['rolling_mean'], color='#C70039')
    AX_DILMA.set_xticklabels(['', '2012', '', '', '2014', '', '', '2016'], alpha=0.3)
    AX_DILMA.text(15300.0, 7.7, 'DILMA', fontsize=18, weight='bold', color='#C70039')
    AX_DILMA.text(14750.0, 7.4, '(2011 - 31/08/2016)', weight='bold', alpha=0.3)

    #plotting for Temer
    AX_TEMER.plot(temer['Time'], temer['rolling_mean'], color='#FF5733')
    AX_TEMER.set_xticklabels(['', '2016', '',  '', '2017', '', '', '2018'], alpha=0.3)
    AX_TEMER.text(17200.0, 7.7, 'TEMER', fontsize=18, weight='bold', color='#FF5733')
    AX_TEMER.text(17100.0, 7.4, '(01/09/2016 - 2018)', weight='bold', alpha=0.3)

    #plotting for Bolsonaro
    AX_BOZO.plot(bozo['Time'], bozo['rolling_mean'], color='#FFC300')
    AX_BOZO.set_xticklabels(['', '2019', '', '', '2020', '', '', '2021'], alpha=0.3)
    AX_BOZO.text(17800.0, 7.7, 'BOLSONARO', fontsize=18, weight='bold', color='#FFC300')
    AX_BOZO.text(17860.0, 7.4, '(2018 - today)', weight='bold', alpha=0.3)

    # plotting for all presidents together
    AX_ALL.plot(fhc['Time'], fhc['rolling_mean'], color='#571845')
    AX_ALL.plot(lula['Time'], lula['rolling_mean'], color='#900C3E')
    AX_ALL.plot(dilma['Time'], dilma['rolling_mean'], color='#C70039')
    AX_ALL.plot(temer['Time'], temer['rolling_mean'], color='#FF5733')
    AX_ALL.plot(bozo['Time'], bozo['rolling_mean'], color='#FFC300')
    AX_ALL.grid(alpha=0.5)
    AX_ALL.set_xticks([])

    # title and subtile being added
    AX_FHC.text(11700.0, 9.5, 'EURO-REAL rate averaged under the last five Brazil presidents',
                fontsize=22, weight='bold')
    AX_FHC.text(11700.0, 8.7, '''EURO-REAL exchange rates under F.H.C (1999 - 2002),
                Lula (2002 - 2010), Dilma (2011 - 2016),
                Temer (2016 - 2018) and Bolsonaro (2018 - today)''',fontsize=16)

    # adding the signature
    AX_ALL.text(10400.0, 0.65, '©Ariel Alsina' + ' '*220 + 'Source: European Central Bank',
            color = '#f0f0f0', backgroundcolor = '#4d4d4d',
            size=14)

    plt.show()


    exchange_rates = exchange_rates[exchange_rates['Brazilian_real'] != '-']
    exchange_rates = exchange_rates[exchange_rates['US_dollar'] != '-']

    exchange_rates['dollar2real'] = exchange_rates['US_dollar'].astype(float) \
                                    / exchange_rates['Brazilian_real'].astype(float)

    # droping the NaN lines
    dollar2real = exchange_rates[['dollar2real', 'Time']]
    dollar2real.dropna(inplace=True)
    dollar2real['rolling_mean'] = get_rolling_window(dollar2real['dollar2real'], 30)

    df_all_brazil_dollar = dollar2real.copy()
    fhc_dollar = df_all_brazil_dollar.copy()[df_all_brazil_dollar['Time'].dt.year < 2002]
    lula_dollar = df_all_brazil_dollar.copy()[(df_all_brazil_dollar['Time'].dt.year >= 2002)
                                            & (df_all_brazil_dollar['Time'].dt.year < 2010)]
    dilma_dollar = df_all_brazil_dollar.copy()[(df_all_brazil_dollar['Time'].dt.year >= 2010)
                                            & (df_all_brazil_dollar['Time'] < '2016-09-01')]
    temer_dollar = df_all_brazil_dollar.copy()[(df_all_brazil_dollar['Time'] >= '2016-09-01')
                                            & (df_all_brazil_dollar['Time'].dt.year < 2018)]
    bozo_dollar = df_all_brazil_dollar.copy()[(df_all_brazil['Time'].dt.year >= 2018)]

    style.use('fivethirtyeight')

    # creating the subplots
    plt.figure(figsize=(20, 10))

    # two rows: one with 3 graphs side-to-side and the second with only a bigger graph
    AX_FHC = plt.subplot(2, 5, 1)
    AX_LULA = plt.subplot(2, 5, 2)
    AX_DILMA = plt.subplot(2, 5, 3)
    AX_TEMER = plt.subplot(2, 5, 4)
    AX_BOZO = plt.subplot(2, 5, 5)
    AX_ALL = plt.subplot(2, 1, 2)

    # changes to all the subplots
    axes = [AX_FHC, AX_LULA, AX_DILMA, AX_TEMER, AX_BOZO, AX_ALL]
    for ax in axes:
        ax.set_ylim(0.0, 1.7)
        ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2])
        ax.set_yticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2'], alpha=0.3)
        ax.grid(alpha=0.5)

    # ploting for FHC
    AX_FHC.plot(fhc_dollar['Time'], fhc_dollar['rolling_mean'], color='#DE3A03')
    AX_FHC.set_xticklabels(['1999', '', '', '2001', '', '', '2002'], alpha=0.3)
    AX_FHC.text(11300.0, 1.4, 'FHC', fontsize=18, weight='bold', color='#DE3A03')
    AX_FHC.text(11200, 1.3, '(1999-2002)', weight='bold', alpha=0.3)

    # plotting for Lula
    AX_LULA.plot(lula_dollar['Time'], lula_dollar['rolling_mean'], color='#F48D03')
    AX_LULA.set_xticklabels(['', '2003', '', '', '', '2007', '', '', '', '2011'], alpha=0.3)
    AX_LULA.text(12700.0, 1.4, 'LULA', fontsize=18, weight='bold', color='#F48D03')
    AX_LULA.text(12430.0, 1.3, '(2002-2010)', weight='bold', alpha=0.3)

    # plotting for Dilma
    AX_DILMA.plot(dilma_dollar['Time'], dilma_dollar['rolling_mean'], color='#E1AF03')
    AX_DILMA.set_xticklabels(['', '2012', '', '', '2014', '', '', '2016'], alpha=0.3)
    AX_DILMA.text(15300.0, 1.4, 'DILMA', fontsize=18, weight='bold', color='#E1AF03')
    AX_DILMA.text(14750.0, 1.3, '(2011 - 31/08/2016)', weight='bold', alpha=0.3)

    #plotting for Temer
    AX_TEMER.plot(temer_dollar['Time'], temer_dollar['rolling_mean'], color='#94E103')
    AX_TEMER.set_xticklabels(['', '2016', '',  '', '2017', '', '', '2018'], alpha=0.3)
    AX_TEMER.text(17200.0, 1.4, 'TEMER', fontsize=18, weight='bold', color='#94E103')
    AX_TEMER.text(17100.0, 1.3, '(01/09/2016 - 2018)', weight='bold', alpha=0.3)

    #plotting for Bolsonaro
    AX_BOZO.plot(bozo_dollar['Time'], bozo_dollar['rolling_mean'], color='#2CA210')
    AX_BOZO.set_xticklabels(['', '2019', '', '', '2020', '', '', '2021'], alpha=0.3)
    AX_BOZO.text(17800.0, 1.4, 'BOLSONARO', fontsize=18, weight='bold', color='#2CA210')
    AX_BOZO.text(17860.0, 1.3, '(2018 - today)', weight='bold', alpha=0.3)

    # plotting for all presidents together
    AX_ALL.plot(fhc_dollar['Time'], fhc_dollar['rolling_mean'], color='#DE3A03')
    AX_ALL.plot(lula_dollar['Time'], lula_dollar['rolling_mean'], color='#F48D03')
    AX_ALL.plot(dilma_dollar['Time'], dilma_dollar['rolling_mean'], color='#E1AF03')
    AX_ALL.plot(temer_dollar['Time'], temer_dollar['rolling_mean'], color='#94E103')
    AX_ALL.plot(bozo_dollar['Time'], bozo_dollar['rolling_mean'], color='#2CA210')
    AX_ALL.grid(alpha=0.5)
    AX_ALL.set_xticks([])

    # title and subtile being added
    AX_FHC.text(11700.0, 2.0, 'DOLLAR-REAL rate averaged under the last five Brazil presidents',
                fontsize=22, weight='bold')
    AX_FHC.text(11700.0, 1.75, '''DOLLAR-REAL exchange rates under F.H.C (1999 - 2002),
                Lula (2002 - 2010), Dilma (2011 - 2016), Temer (2016 - 2018) 
                and Bolsonaro (2018 - today)''',fontsize=16)

    # adding the signature
    AX_ALL.text(10400.0, 0.0, '©Ariel Alsina' + ' '*220 + 'Source: European Central Bank',
            color = '#f0f0f0', backgroundcolor = '#4d4d4d',
            size=14)

    plt.show()
