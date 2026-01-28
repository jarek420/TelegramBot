import os
from datetime import timedelta

import pandas as pd
import yfinance as yf

TICKERS = {
    "Gold": "GC=F",
    "Silver": 'SI=F',
    "Bitcoin ": "BTC-USD",
    "USD/PLN": "PLNUSD=X",
    "US100 ": "^NDX"
}

INTERVAL = "1h"
PERIOD = "30d"
OUT_DIR = "charts"

def nearest_value(close: pd.Series, ts: pd.Timestamp) -> float:
    idx = close.index
    pos = idx.get_indexer([ts], method="nearest")[0]
    return float(close.iloc[pos])

def fetch_last_and_change(symbol: str, hours: int = 24):
    df = yf.download(symbol, period=PERIOD, interval=INTERVAL, progress=False, auto_adjust=True)
    if df is None or df.empty or "Close" not in df:
        raise RuntimeError("Brak danych")
    close = df["Close"].dropna()
    last_ts = close.index[-1]
    last = float(close.iloc[-1])

    past_ts = last_ts - timedelta(hours=hours)
    past = nearest_value(close, past_ts)

    abs_change = last - past
    pct_change = (abs_change / past) * 100.0 if past != 0 else float("nan")

    return last, abs_change, pct_change, last_ts, past_ts


def get_data():
    rows = []
    for name, sym in TICKERS.items():
        try:
            last, abs_chg, pct_chg, last_ts, past_ts = fetch_last_and_change(sym, hours=25)
            if pct_chg < 0:
                rows.append(f"🟥 {name}: {round(last,2)} USD | 24h: {round(pct_chg, 2)} % 🟥")
            elif pct_chg > 0:
                rows.append(f"🟩{name}: {round(last,2)} USD | 24h: {round(pct_chg, 2)} % 🟩")
        except Exception as e:
            rows.append({
                "Instrument": name,
                "Symbol": sym,
                "Error": str(e),
            })

    return rows

def get_stock_message():
    data = get_data()
    message = "\t\tYAHOO index: \n"

    data = get_data()
    for i in data:
        for x in i:
            message += x
        message += "\n"
    
    return message

def main():
    rows = []
    for name, sym in TICKERS.items():
        try:
            last, abs_chg, pct_chg, last_ts, past_ts = fetch_last_and_change(sym, hours=25)
            rows.append({
                "Instrument": name,
                "Symbol": sym,
                "Last": round(last, 6),
                "Change 24h": round(abs_chg, 6),
                "Change 24h %": round(pct_chg, 4),
            })
        except Exception as e:
            rows.append({
                "Instrument": name,
                "Symbol": sym,
                "Error": str(e),
            })
    
    print(rows)

if __name__ == "__main__":
    d = get_data()
    for i in d:
        print(i)