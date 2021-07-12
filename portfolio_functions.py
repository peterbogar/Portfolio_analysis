# Functions for Portfolio analysis

import yfinance as yf
import pandas as pd


def download(symbols, start_date, end_date):
    # Function to download close price for symbols for specified date window from Yahoo or from file
    # Input: list of symbols, start date, end date
    # Output: dataframe with close price for each day
    # Usage: download(list of symbols, '2020-01-01', '2020-12-31')

    # Read data from Yahoo
    df = yf.download(symbols, start_date, end_date)
    # Read only 'Adj price' for each symbol
    df_data_download = df[[("Adj Close", s) for s in symbols]]
    # Remove two level header
    df_data_download.columns = df_data_download.columns.droplevel(level=0)
    # df_close_prices.to_csv('downloaded_data.csv')

    # Read data from file
    # df_data_download = pd.read_csv('downloaded_data.csv', index_col=0)

    return df_data_download


def stock_return(symbols, df_stock_return):
    # Function to calculate return for 1 long stock for each symbol
    # Input: list of symbols, dataframe with close prices
    # Output: to input dataframe added total absolut return and total % return
    # Usage: stock_return(list of symbols, df_data_download)

    for symbol in symbols:
        df_stock_return[symbol + '_cumulative_gain'] = df_stock_return[symbol] - df_stock_return[symbol].values[0]
        df_stock_return[symbol + '_cumulative_gain%'] = (df_stock_return[symbol + '_cumulative_gain'] / df_stock_return[symbol].values[0])

    return df_stock_return


def stock_volatility(symbols, df_stock_volatility):
    # Function for calculate annualized volatility of returns for each symbol
    # Input: list of symbols, dataframe with close prices
    # Output: to input dataframe add daily gain and its volatility: volatility = std(daily_gain) * sqrt(252)
    # Usage: stock_volatility(list of symbols, df_stock_return)

    for symbol in symbols:
        df_stock_volatility[symbol + '_daily_gain'] = df_stock_volatility[symbol]/df_stock_volatility[symbol].shift(1) - 1
    df_stock_volatility.fillna(0, inplace=True)

    for symbol in symbols:
        df_stock_volatility[symbol + '_volatility%'] = (df_stock_volatility[symbol + '_daily_gain'].std()) * (252**(1/2))

    return df_stock_volatility


def stock_sharpe_ratio(symbols, time_period, df_stock_sharpe_ratio):
    # Function to calculating Sharpe ratio for each stock: sharpe ratio = (return/time period - risk free return) / volatility
    # Input: symbols, time period, dataframe with gain in and volatility for each stock
    # Output: to input dataframe add Sharpe ratio
    # Usage: stock_sharpe_ratio(list of symbols, time_period, df_stock_volatility)

    # Risk free rate is set to 3%, TODO: opravit
    risk_free_rate = 0.03

    for symbol in symbols:
        df_stock_sharpe_ratio[symbol + '_sharpe_ratio'] = ((df_stock_sharpe_ratio[symbol + '_cumulative_gain%'].values[-1] / time_period) - risk_free_rate) / df_stock_sharpe_ratio[symbol + '_volatility%'].values[-1]

    return df_stock_sharpe_ratio


def stock_drawdown(symbols, df_stock_drawdown):
    # Function to calculate max drawdown for each stock: drawdown = (current price/highest price so far) -1
    # Input: list of symbols, dataframe with close prices
    # Output: to input dataframe add max drawdown (one number)
    # Usage: stock_drawdown(symbols, df_stock_sharpe_ratio)

    for symbol in symbols:
        df_stock_drawdown[symbol + '_highest_price'] = df_stock_drawdown[symbol].cummax()
        df_stock_drawdown[symbol + '_drawdown%'] = (df_stock_drawdown[symbol] / df_stock_drawdown[symbol + '_highest_price']) - 1
        df_stock_drawdown[symbol + '_max_drawdown%'] = df_stock_drawdown[symbol + '_drawdown%'].min()

    return df_stock_drawdown


def stock_get_perfromance(symbols, time_period, df_stock_drawdown):
    # Function to collect performance data for each stock from raw dataframe
    # Input: symbols, time period (in years), dataframe with cumulative return, volatility, max drawdown, sharpe ratio for each symbol
    # Output: dataframe with columns (avg annual return, volatility, max drawdown, sharpe ratio) and rows (each symbol)
    # Usage: stock_get_perfromance(symbols, time_period, df_stock_drawdown)

    # Defining output dataframe
    df_stock_performance = pd.DataFrame({'Avg Annual Return %': [''], 'Volatility %': [''], 'Max Drawdown %': [''], 'Sharpe Ratio': ['']}, index=symbols)

    for symbol in symbols:
        df_stock_performance.loc[symbol, 'Avg Annual Return %'] = (df_stock_drawdown[symbol + '_cumulative_gain%'].values[-1] * 100 / time_period).round(2)
        df_stock_performance.loc[symbol, 'Volatility %'] = (df_stock_drawdown[symbol + '_volatility%'].values[-1] * 100).round(2)
        df_stock_performance.loc[symbol, 'Max Drawdown %'] = (df_stock_drawdown[symbol + '_max_drawdown%'].values[-1] * 100).round(2)
        df_stock_performance.loc[symbol, 'Sharpe Ratio'] = (df_stock_drawdown[symbol + '_sharpe_ratio'].values[-1]).round(2)

    return df_stock_performance
