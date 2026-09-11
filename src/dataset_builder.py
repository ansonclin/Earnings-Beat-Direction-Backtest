import pandas as pd
from earnings_loader import get_earnings_report
from price_loader import get_price_window, get_pre_post_earnings_closes, compute_pct_reaction
from features import get_historical_volatility

tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "JPM", "V", "JNJ", "WMT", "HD", "DIS", "KO", "PG"]
rows = [] # to store and create pandas dataframe

for ticker in tickers:
    report = get_earnings_report(ticker)
    for earnings_date, row in report.iterrows():
        estimate = row["EPS Estimate"]
        actual = row["Reported EPS"]

        if pd.isna(estimate) or pd.isna(actual): # checks if isna is "NaN"
            continue

        surprise = (actual - estimate) / estimate * 100
        prices = get_price_window(ticker, earnings_date)
        before, after = get_pre_post_earnings_closes(prices, earnings_date)
        pct_reaction = compute_pct_reaction(before, after)
        direction = "up" if pct_reaction > 0 else "down"
        historical_volatility = get_historical_volatility(ticker, earnings_date)

        rows.append({
            "ticker": ticker,
            "earnings_date": earnings_date,
            "surprise": surprise,
            "pct_reaction": pct_reaction,
            "direction": direction,
            "historical_volatility": historical_volatility,
        })

dataset = pd.DataFrame(rows) 
print(dataset)
