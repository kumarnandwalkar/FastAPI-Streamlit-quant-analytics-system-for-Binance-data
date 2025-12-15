def check_zscore_alert(zscore_series, threshold=2.0):
    if zscore_series.empty:
        return None

    latest = zscore_series.iloc[-1]

    if abs(latest) >= threshold:
        return {
            "triggered": True,
            "value": float(latest),
            "threshold": threshold
        }

    return {"triggered": False}
