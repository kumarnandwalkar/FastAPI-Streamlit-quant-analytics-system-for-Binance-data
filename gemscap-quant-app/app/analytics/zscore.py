import pandas as pd

def zscore(series: pd.Series, window: int = 50) -> pd.Series:
    if len(series) < window:
        return pd.Series(dtype=float)

    mean = series.rolling(window).mean()
    std = series.rolling(window).std()

    z = (series - mean) / std
    return z.dropna()
