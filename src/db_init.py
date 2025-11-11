from pathlib import Path
import duckdb

DB_PATH = Path("data/db/mstr_btc.duckdb")

DDL = """
CREATE TABLE IF NOT EXISTS prices (
    date DATE PRIMARY KEY,
    mstr_close DOUBLE,
    btc_usd_close DOUBLE,
    ibit_close DOUBLE,
    source VARCHAR,
    "asof" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
    date DATE,
    type VARCHAR,
    subtype VARCHAR,
    title VARCHAR,
    amount_usd DOUBLE,
    shares DOUBLE,
    coupon DOUBLE,
    conv_price DOUBLE,
    maturity DATE,
    source VARCHAR,
    notes VARCHAR,
    "asof" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS meta (
    key VARCHAR PRIMARY KEY,
    value VARCHAR,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(DB_PATH.as_posix())
    con.execute(DDL)
    con.close()
    print(f"✅ Initialized full schema at {DB_PATH}")

if __name__ == "__main__":
    main()
