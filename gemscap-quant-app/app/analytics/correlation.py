import pandas as pd

def rolling_corr(x: pd.Series, y: pd.Series, window: int = 50) -> pd.Series:
    df = pd.concat([x, y], axis=1).dropna()

    if len(df) < window:
        return pd.Series(dtype=float)

    return df.iloc[:, 0].rolling(window).corr(df.iloc[:, 1])
