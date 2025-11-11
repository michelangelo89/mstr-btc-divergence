# src/db_utils.py
from pathlib import Path
import duckdb
import pandas as pd

# Resolve repo root as the parent of src/
REPO_ROOT = Path(__file__).resolve().parents[1]
DB = REPO_ROOT / "data" / "db" / "mstr_btc.duckdb"

def read_prices() -> pd.DataFrame:
    if not DB.exists():
        raise FileNotFoundError(f"❌ Database not found at: {DB.resolve()}")
    
    print(f"✅ Reading DB from: {DB.resolve()}")
    con = duckdb.connect(DB.as_posix(), read_only=True)
    df = con.execute("""
        SELECT date, mstr_close, btc_usd_close, ibit_close
        FROM prices
        ORDER BY date
    """).df()
    con.close()
    df = df.set_index("date").rename_axis("date")
    return df