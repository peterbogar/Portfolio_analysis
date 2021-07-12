# Functions

import yfinance as yf
import pandas as pd


def download(symbols, start_date, end_date):
    # Function to download close price for symbols for specified date window from Yahoo
    # Usage: download(['AAPL', 'SPY'], '2020-01-01', '2020-12-31')

    # Read data from Yahoo
    df = yf.download(symbols, start_date, end_date)
    df_data_download = df[[("Adj Close", s) for s in symbols]]
    df_data_download.columns = df_data_download.columns.droplevel(level=0)
    # df_close_prices.to_csv('downloaded_data.csv')

    # Read data from file
    # df_data_download = pd.read_csv('downloaded_data.csv', index_col=0)

    return df_data_download


def stock_return(symbols, df_stock_return):
    # Function to calculate return for 1 long stock for each symbol

    for symbol in symbols:
        # print(df_stock_return[symbol].values[0])
        # print(df_stock_return[symbol].values[-1])
        df_stock_return[symbol + '_cumulative_gain'] = df_stock_return[symbol] - df_stock_return[symbol].values[0]
        df_stock_return[symbol + '_cumulative_gain%'] = (df_stock_return[symbol + '_cumulative_gain'] / df_stock_return[symbol].values[0])

    return df_stock_return


def stock_volatility(symbols, df_stock_volatility):
    # Function for calculate volatility of returns for single stock
    # volatility = std(daily_gain) * sqrt(252)

    for symbol in symbols:
        df_stock_volatility[symbol + '_daily_gain'] = df_stock_volatility[symbol]/df_stock_volatility[symbol].shift(1) - 1
    df_stock_volatility.fillna(0, inplace=True)

    for symbol in symbols:
        df_stock_volatility[symbol + '_volatility%'] = (df_stock_volatility[symbol + '_daily_gain'].std()) * (252**(1/2))

    return df_stock_volatility


def stock_sharpe_ratio(symbols, time_period, df_stock_sharpe_ratio):
    # Function to calculating Sharpe ratio for 1 stock
    # sharpe ratio = (return - risk free return) / volatility

    risk_free_rate = 0.03

    for symbol in symbols:
        df_stock_sharpe_ratio[symbol + '_sharpe_ratio'] = ((df_stock_sharpe_ratio[symbol + '_cumulative_gain%'].values[-1] / time_period) - risk_free_rate) / df_stock_sharpe_ratio[symbol + '_volatility%'].values[-1]

    return df_stock_sharpe_ratio


def stock_drawdown(symbols, df_stock_drawdown):
    # Function to calculate max drawdown
    # drawdown = (current price/highest price so far) -1

    for symbol in symbols:
        df_stock_drawdown[symbol + '_highest_price'] = df_stock_drawdown[symbol].cummax()
        df_stock_drawdown[symbol + '_drawdown%'] = (df_stock_drawdown[symbol] / df_stock_drawdown[symbol + '_highest_price']) - 1
        df_stock_drawdown[symbol + '_max_drawdown%'] = df_stock_drawdown[symbol + '_drawdown%'].min()

    return df_stock_drawdown


def stock_get_perfromance(symbols, time_period, df_stock_drawdown):
    # Function to collect performance data for each stock from raw dataframe

    df_stock_performance = pd.DataFrame({'Avg Annual Return %': [''], 'Volatility %': [''], 'Max Drawdown %': [''], 'Sharpe Ratio': ['']}, index=symbols)

    for symbol in symbols:
        df_stock_performance.loc[symbol, 'Avg Annual Return %'] = (df_stock_drawdown[symbol + '_cumulative_gain%'].values[-1] * 100 / time_period).round(2)
        df_stock_performance.loc[symbol, 'Volatility %'] = (df_stock_drawdown[symbol + '_volatility%'].values[-1] * 100).round(2)
        df_stock_performance.loc[symbol, 'Max Drawdown %'] = (df_stock_drawdown[symbol + '_max_drawdown%'].values[-1] * 100).round(2)
        df_stock_performance.loc[symbol, 'Sharpe Ratio'] = (df_stock_drawdown[symbol + '_sharpe_ratio'].values[-1]).round(2)

    return df_stock_performance
