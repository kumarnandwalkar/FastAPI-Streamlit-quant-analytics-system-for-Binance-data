import pandas as pd

def compute_spread(y: pd.Series, x: pd.Series, beta: float) -> pd.Series:
    """
    Computes spread = y - beta * x
    Assumes y and x are already time-aligned.
    """
    df = pd.concat([y, x], axis=1).dropna()
    return df.iloc[:, 0] - beta * df.iloc[:, 1]
    