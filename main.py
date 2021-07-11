# Main script

import pandas as pd
import matplotlib.pyplot as plt
from portfolio_functions import download
from portfolio_functions import stock_gain
from portfolio_functions import stock_volatility
from portfolio_functions import stock_sharpe_ratio
from portfolio_functions import stock_drawdown


# Display all columns in pandas dataframe
pd.set_option('display.max_columns', None)


initial_account = 10000
start_date = '2020-01-02'
end_date = '2020-12-31'
symbols = ['AAPL', 'SPY', 'QQQ', 'GLD', 'TLT']


if __name__ == '__main__':

    df_data_download = download(symbols, start_date, end_date)
    # print()
    # print(df_data_download)
    # print()
    # print('Correlation:')
    # df_corr = df_data_download.corr()
    # print(df_corr.round(2))
    df_stock_return = stock_gain(symbols, df_data_download)
    # print()
    # print(df_stock_return)
    df_stock_volatility = stock_volatility(symbols, df_stock_return)
    # print()
    # print(df_stock_volatility)
    df_stock_sharpe_ratio = stock_sharpe_ratio(symbols, df_stock_volatility)
    # print()
    # print(df_stock_sharpe_ratio)
    df_stock_drawdown = stock_drawdown(symbols, df_stock_sharpe_ratio)
    # print()
    # print(df_stock_drawdown)
    # df_stock_drawdown.to_excel('output.xlsx')

    df_chart = df_stock_drawdown[['AAPL_cumulative_gain%', 'AAPL_drawdown%']]
    df_chart.plot()
    plt.show()
