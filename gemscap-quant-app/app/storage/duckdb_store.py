import duckdb
import pandas as pd
from app.config import DUCKDB_PATH

conn = duckdb.connect(DUCKDB_PATH)

def init_db():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            symbol VARCHAR,
            ts TIMESTAMP,
            price DOUBLE,
            size DOUBLE
        )
    """)

def insert_ticks(ticks: list[dict]):
    if not ticks:
        return
    df = pd.DataFrame(ticks)
    conn.execute("INSERT INTO ticks SELECT * FROM df")
