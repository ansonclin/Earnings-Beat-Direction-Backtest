import pandas as pd 
import yfinance as yt

def classify_report_time(earnings_date):
    if earnings_date.hour < 9:
        return "BMO"
    elif 9 <= earnings_date.hour <= 15:
        return "DURING_MARKET"
    else:
        return "AMC"
    
def get_price_window(ticker, earnings_date):
    stock = yt.Ticker(ticker)
    start = earnings_date - pd.Timedelta(days = 7)
    end = earnings_date + pd.Timedelta(days = 7)
    prices = stock.history(start = start, end = end)
    return prices 

def get_pre_post_earnings_closes(prices, earnings_date):
    classification = classify_report_time(earnings_date)
    earnings_day = earnings_date.normalize() # normalize to start time to midnight 

    if classification == "AMC": # After market closure: (before days is current day and after day is next day)
        before_days = prices[prices.index <= earnings_day] # price.index grabs the dates of prices and returns all dates before earnings_day (hence <=)
        after_days = prices[prices.index > earnings_day] 
    else: # BMO
        before_days = prices[prices.index < earnings_day]
        after_days = prices[prices.index >= earnings_day]

    before_close = before_days["Close"].iloc[-1] # last row of before_days before earnigns date. (already in order because of stock.history())
    after_close = after_days["Close"].iloc[0]

    return before_close, after_close

def compute_pct_reaction(before_close, after_close):
    return (after_close - before_close)/before_close * 100