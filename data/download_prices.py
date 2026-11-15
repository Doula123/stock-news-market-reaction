import pandas as pd
import yfinance as yf

# Date, Tickers
membership = pd.read_csv("sp500_tickers.csv")
membership.columns = ["date", "tickers"]
membership["date"] = pd.to_datetime(membership["date"])

ranking_date = pd.Timestamp("2024-06-07")
eligible = membership[membership["date"] <= ranking_date]
snapshot = eligible.sort_values("date").iloc[-1]

# Yahoo Finance uses BRK-B instead of BRK.B.
tickers = [
    ticker.strip().replace(".", "-")
    for ticker in snapshot["tickers"].split(",")
]

print(f"Membership snapshot: {snapshot['date'].date()}")
print(f"Requesting prices for {len(tickers)} stocks")

data = yf.download(
    tickers,
    start="2020-01-01",
    end="2024-07-01",
    interval="1d",
    auto_adjust=True,
)

if data is None or data.empty:
    raise RuntimeError("No price data downloaded.")

prices = data["Close"].dropna(axis=1, how="all")
prices.to_csv("daily_prices.csv")

missing = sorted(set(tickers) - set(prices.columns))
print(f"Saved prices for {len(prices.columns)} stocks to daily_prices.csv")
print(f"Tickers with no prices: {missing}")