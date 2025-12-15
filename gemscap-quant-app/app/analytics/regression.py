import numpy as np
import pandas as pd

def hedge_ratio(x: pd.Series, y: pd.Series) -> float:
    """
    Computes OLS hedge ratio (beta) for y ~ beta * x
    """

    df = pd.concat([x, y], axis=1).dropna()

    if len(df) < 10:
        return 0.0

    cov = np.cov(df.iloc[:, 0], df.iloc[:, 1])[0, 1]
    var = np.var(df.iloc[:, 0])

    return cov / var if var != 0 else 0.0

def rolling_hedge_ratio(x, y, window=50):
    df = pd.concat([x, y], axis=1).dropna()

    return (
        df.iloc[:, 1]
        .rolling(window)
        .cov(df.iloc[:, 0]) /
        df.iloc[:, 0].rolling(window).var()
    )

