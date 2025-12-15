import pandas as pd

def resample_ticks(df: pd.DataFrame, interval: str = "1s") -> pd.Series:
    """
    Resamples tick data to equally spaced bars.
    Returns LAST traded price per interval.
    """

    if df.empty:
        return pd.Series(dtype=float)

    df = df.copy()
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df = df.set_index("ts")

    price_series = (
        df["price"]
        .resample(interval)
        .last()
        .ffill()
        .dropna()
    )

    return price_series
