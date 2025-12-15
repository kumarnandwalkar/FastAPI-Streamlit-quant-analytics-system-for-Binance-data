import numpy as np
import pandas as pd

def half_life(spread: pd.Series):
    spread_lag = spread.shift(1).dropna()
    delta = spread.diff().dropna()

    beta = np.polyfit(spread_lag, delta, 1)[0]
    if beta >= 0:
        return None

    return -np.log(2) / beta
