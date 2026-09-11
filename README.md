# Earnings Beat Direction Backtest

## Purpose

Backtest a common assumption — "if a company beats earnings estimates, the stock goes up" — against real historical outcomes, using only information knowable *before* each report.

Most people treat that assumption as close to a rule. This project checks it directly: for every earnings event in the dataset, did a beat actually correspond to the stock going up, and did a miss actually correspond to it going down? The answer is measured, not assumed.

## Repo layout
```
Earnings_reaction/
├── src/
│   ├── earnings_loader.py             # pulls earnings dates + estimated/actual EPS per ticker via yfinance
│   ├── price_loader.py                # computes % price reaction, handling before/after-market-close report timing
│   ├── dataset_builder.py             # combines earnings + price data into one table, one row per earnings event
│   ├── features.py                    # historical volatility (pre-earnings only, computed but not used in the current analysis)
│   └── beat_direction_correlation.py  # backtests beat/miss against up/down, prints the real percentages
├── requirements.txt
├── results.json                        # real backtested results
└── README.md
```

## Tech Stack / Libraries
**Python** — pandas (data wrangling), yfinance (earnings + price data, no API key required)

## Technicals

The pipeline starts with `earnings_loader.py`, which pulls each ticker's earnings history via yfinance's `get_earnings_dates()` — estimated EPS, actual EPS, and a timestamp for when the report was released.

That timestamp turned out to matter more than expected. Companies report either **before market open (BMO)** or **after market close (AMC)**, and which one determines which two trading days' closing prices actually bracket the reaction. If a company reports after close, the "before" price is that day's close and the "after" price is the next trading day's close — the market hasn't had a chance to react yet. If a company reports before market open, the entire next trading session already reflects the news, so the "before" price has to be the *prior* day's close instead. Getting this wrong silently shifts the measured reaction by a full trading day, which either dilutes the real move or captures pure noise instead. `price_loader.py` classifies each report as BMO/AMC from the timestamp's hour (verified empirically against known BMO reporters like JNJ and WMT vs. known AMC reporters like AAPL and MSFT), then picks the correct pair of closing prices before computing `% reaction = (after - before) / before * 100`.

`dataset_builder.py` combines both sources into one table — one row per (ticker, earnings date), with `surprise` (`(actual EPS - estimated EPS) / estimated EPS * 100`), the computed `% reaction`, and `direction` (up/down, derived from the sign of the reaction).

`beat_direction_correlation.py` is the actual analysis: split the dataset into "beat" events (`surprise > 0`) and "miss" events (`surprise < 0`), then check, within each group, how often `direction` actually matched what you'd expect (up for a beat, down for a miss). No model, no training — just a direct count of how often the assumption held true across real historical events.

## Results

Across 360 backtested earnings events (15 tickers, 2020–2026):

- **303 beat events** — of those, only **53.5%** actually went up
- **43 miss events** — of those, **72.1%** actually went down
- **Overall, the "beat = up, miss = down" assumption held true 53.6%** of the time

Beats were far more common than misses (303 vs. 43) — companies beat estimates most of the time, a well-documented pattern (guidance is often set to be beatable). But when they do beat, it's barely better than a coin flip whether the stock actually goes up.

## Problems Encountered

**BMO/AMC timing ambiguity.** Described above under Technicals — this was the single trickiest correctness issue in the project, since getting it wrong doesn't throw an error, it just silently measures the wrong thing.

## Known Limitations

**Correlation, not causation, and no other factors considered.** This only checks whether beat/miss lines up with direction — it says nothing about *why*, and ignores guidance, sector trends, macro conditions, or anything said on the earnings call. A real example: AAPL beat estimates by +6.88% on 2026-07-30, and the stock still dropped 7.35% — exactly the kind of case this simple check can't explain.

**Sample size is uneven between groups.** 303 beat events vs. only 43 miss events — the miss group's 72.1% figure is based on a much smaller sample and is less statistically solid than the beat group's 53.5%.

**The result is a modest one.** 53.6% overall is only slightly better than random guessing on a binary outcome. That's the honest finding, not a strong edge.

## Installation

### Prerequisites
- Python + pip

### 1. Clone the repo
```
git clone <repo-url>
cd Earnings_reaction
```

### 2. Set up the environment
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
No API keys or `.env` file needed — yfinance doesn't require authentication.

### 3. Run the analysis
```
cd src
python3 beat_direction_correlation.py
```
This pulls fresh data for all 15 tickers (takes a couple of minutes), builds the dataset, and prints the real beat/miss vs. up/down percentages.
