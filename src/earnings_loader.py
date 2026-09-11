import yfinance as yt

tickers = ["AAPL", "MSFT", "NVDA"]

def get_earnings_report(ticker):
    stock = yt.Ticker(ticker)
    report = stock.get_earnings_dates(limit=12)
    return report

for ticker in tickers:
    report = get_earnings_report(ticker)
    if report is None or report.empty:
        continue

    print(f"--- {ticker} ---")
    print(report)
