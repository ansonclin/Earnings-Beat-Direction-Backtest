import pandas as pd
import yfinance as yt

def get_historical_volatility(ticker, earnings_date, window=30):
    stock = yt.Ticker(ticker)
    start = earnings_date - pd.Timedelta(days=50)   # buffer big enough for 30 trading days
    end = earnings_date - pd.Timedelta(days=1)      # ends before the earnings date, how far back?

    prices = stock.history(start=start, end=end)
    daily_returns = prices["Close"].pct_change()
    volatility = daily_returns.tail(window).std()
    return volatility
