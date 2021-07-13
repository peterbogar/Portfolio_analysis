# Main script
# 1. download daily data for selected stocks
# 2. calculating performance data if holding one stock from each symbol: corelation, total return, avg annual return, volatility, max drawdown, Sharpe ratio
# TODO: header in excel

import pandas as pd
import datetime as dt
# import matplotlib.pyplot as plt
from tabulate import tabulate
from portfolio_functions import check_history
from portfolio_functions import download
from portfolio_functions import stock_return
from portfolio_functions import stock_volatility
from portfolio_functions import stock_sharpe_ratio
from portfolio_functions import stock_drawdown
from portfolio_functions import stock_get_perfromance


# Display all columns in pandas dataframe
pd.set_option('display.max_columns', None)

# Initial variables
initial_account = 10000
start_date = '2019-03-20'
end_date = '2021-07-01'
# symbols = ['AAPL', 'FB', 'SPY']
dow_jones = ['MMM', 'AXP', 'AMGN', 'AAPL', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DOW', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'MCD', 'MRK', 'MSFT', 'NKE', 'PG', 'CRM', 'TRV', 'UNH', 'VZ', 'V', 'WBA', 'WMT', 'DIS']
symbols = dow_jones


def stock_perf():
    # Downloading data for each stock
    df_data_download = download(symbols, start_date, end_date)
    print(df_data_download)

    # Calculating correlation among stocks
    df_corr = df_data_download.corr().round(2)

    # Calculating return for each stocks
    df_stock_return = stock_return(symbols, df_data_download)

    # Calculating volatility for each stocks
    df_stock_volatility = stock_volatility(symbols, df_stock_return)

    # Calculating Sharpe ratio for enach stocks
    df_stock_sharpe_ratio = stock_sharpe_ratio(symbols, time_period, df_stock_volatility)

    # Calculating drawdown for single stocks
    df_stock_drawdown = stock_drawdown(symbols, df_stock_sharpe_ratio)

    # Write raw results to a file
    # df_stock_drawdown.to_excel('output.xlsx')

    # Table output
    print()
    print('Stock Correlation:')
    print(tabulate(df_corr, headers='keys', tablefmt='fancy_grid'))
    writer = pd.ExcelWriter('output.xlsx')
    df_corr.to_excel(writer, 'Correlation')

    print()
    print('Stock performance:')
    print('From date: ', start_date)
    print('To date: ', end_date)
    print(round(time_period, 2), 'years')
    df_perf = stock_get_perfromance(symbols, time_period, df_stock_drawdown)
    print(tabulate(df_perf, headers='keys', tablefmt='fancy_grid'))
    df_perf.to_excel(writer, 'Performance')
    writer.save()

    # Chart output
    # df_chart = df_stock_drawdown[['AAPL_cumulative_gain%', 'AAPL_drawdown%']]
    # df_chart.plot()
    # plt.show()


if __name__ == '__main__':

    # Time period in years to download data
    time_period = (dt.datetime.strptime(end_date, '%Y-%m-%d') - dt.datetime.strptime(start_date, '%Y-%m-%d')).days / 365

    # History check
    if check_history(symbols, start_date):
        stock_perf()
