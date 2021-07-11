# Functions

import yfinance as yf
import pandas as pd


def download(symbols, start_date, end_date):
    # Function to download close price for symbols for specified date window from Yahoo
    # Usage: download(['AAPL', 'SPY'], '2020-01-01', '2020-12-31')

    # Read data from Yahoo
    # df = yf.download(symbols, start_date, end_date)
    # df_close_prices = df[[("Adj Close", s) for s in symbols]]
    # df_close_prices.columns = df_close_prices.columns.droplevel(level=0)
    # df_close_prices.to_csv('downloaded_data.csv')

    # Read data from file
    df_close_prices = pd.read_csv('downloaded_data.csv', index_col=0)

    return df_close_prices


def stock_gain(symbols, df_data_download):
    # Function to calculate return for 1 long stock for each symbol

    for symbol in symbols:
        # print(df_data_download[symbol].values[0])
        # print(df_data_download[symbol].values[-1])
        df_data_download[symbol + '_cumulative_gain'] = df_data_download[symbol] - df_data_download[symbol].values[0]
        df_data_download[symbol + '_cumulative_gain%'] = (df_data_download[symbol + '_cumulative_gain'] / df_data_download[symbol].values[0])

    return df_data_download


def stock_volatility(symbols, df_stock_return):
    # Function for calculate volatility of returns for single stock
    # volatility = std(daily_gain) * sqrt(252)

    for symbol in symbols:
        df_stock_return[symbol + '_daily_gain'] = df_stock_return[symbol]/df_stock_return[symbol].shift(1) - 1
    df_stock_return.fillna(0, inplace=True)

    for symbol in symbols:
        df_stock_return[symbol + '_volatility%'] = (df_stock_return[symbol + '_daily_gain'].std()) * (252**(1/2))

    return df_stock_return


def stock_sharpe_ratio(symbols, df_stock_volatility):
    # Function to calculating Sharpe ratio for 1 stock
    # sharpe ratio = (return - risk free return) / volatility

    risk_free_rate = 0.03

    for symbol in symbols:
        df_stock_volatility[symbol + '_sharpe_ratio'] = (df_stock_volatility[symbol + '_cumulative_gain%'].values[-1] - risk_free_rate) / df_stock_volatility[symbol + '_volatility%'].values[-1]

    return df_stock_volatility


def stock_drawdown(symbols, df_stock_sharpe_ratio):
    # Function to calculate max drawdown
    # drawdown = (current price/highest price so far) -1

    for symbol in symbols:
        df_stock_sharpe_ratio[symbol + '_highest_price'] = df_stock_sharpe_ratio[symbol].cummax()
        df_stock_sharpe_ratio[symbol + '_drawdown%'] = (df_stock_sharpe_ratio[symbol] / df_stock_sharpe_ratio[symbol + '_highest_price']) -1

    return df_stock_sharpe_ratio
