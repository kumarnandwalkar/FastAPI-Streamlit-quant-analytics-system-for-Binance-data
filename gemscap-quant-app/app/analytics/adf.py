from statsmodels.tsa.stattools import adfuller

def adf_test(series):
    result = adfuller(series.dropna())
    return {
        "adf_stat": result[0],
        "p_value": result[1]
    }
