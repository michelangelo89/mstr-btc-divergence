from datetime import datetime, timezone
import pandas as pd
import duckdb, yfinance as yf

DB = "data/db/mstr_btc.duckdb"

TICKERS = {
    "MSTR": "mstr_close",
    "BTC-USD": "btc_usd_close",
    # "IBIT": "ibit_close",  # enable when you want the ETF as well
}

def fetch_hist(ticker: str, start: str, end: str) -> pd.Series:
    df = yf.Ticker(ticker).history(start=start, end=end, interval="1d", auto_adjust=True)
    if df.empty:
        return pd.Series(dtype=float, name=ticker)
    s = df["Close"].copy()
    s.index = pd.to_datetime(s.index).tz_localize(None)  # naive timestamps
    s.name = ticker
    return s

def main():
    asof = datetime.now(timezone.utc)
    con = duckdb.connect(DB)

    last = con.execute("SELECT COALESCE(MAX(date), DATE '1970-01-01') FROM prices").fetchone()[0]
    last = pd.to_datetime(last)
    start = (last + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    end   = datetime.now().strftime("%Y-%m-%d")

    if start > end:
        print("No new dates to fetch.")
        con.close()
        return

    frames = []
    for tk, col in TICKERS.items():
        s = fetch_hist(tk, start, end)
        if not s.empty:
            frames.append(s.rename(col).to_frame().reset_index().rename(columns={"Date":"date"}))

    if not frames:
        print("Nothing fetched.")
        con.close()
        return

    out = frames[0]
    for f in frames[1:]:
        out = out.merge(f, on="date", how="outer")

    # ensure all columns exist for insert
    for c in ["mstr_close","btc_usd_close","ibit_close"]:
        if c not in out.columns:
            out[c] = None

    out = out.sort_values("date").reset_index(drop=True)
    out["source"] = "yahoo"
    out["asof"] = asof

    con.execute("""
        INSERT OR REPLACE INTO prices
        SELECT date, mstr_close, btc_usd_close, ibit_close, source, "asof"
        FROM out
    """)
    con.close()
    print(f"Upserted {len(out)} rows into prices")

if __name__ == "__main__":
    main()
