import pandas as pd
import logging
from app.analytics.adf import adf_test

logger = logging.getLogger(__name__)

MIN_POINTS = 60

def signal_quality(
    spread: pd.Series,
    y: pd.Series,
    x: pd.Series,
    volume: pd.Series,
    hedge_ratio_series: pd.Series
):
    try:
        # ------------------------------
        # Guard: insufficient data
        # ------------------------------
        if len(spread.dropna()) < MIN_POINTS:
            return {
                "quality": "LOW",
                "reason": "Insufficient data",
                "stationary": False,
                "correlation": None,
                "hedge_ratio_stable": False,
                "liquidity_ok": False
            }

        result = {}

        # ------------------------------
        # 1️⃣ Stationarity (ADF)
        # ------------------------------
        spread_clean = spread.dropna()
        adf = adf_test(spread_clean)
        result["stationary"] = adf["p_value"] < 0.05
        result["adf_p_value"] = adf["p_value"]

        # ------------------------------
        # 2️⃣ Correlation
        # ------------------------------
        corr_series = y.rolling(50).corr(x)
        corr = corr_series.dropna().iloc[-1]
        result["correlation"] = float(corr)
        result["correlation_ok"] = corr > 0.7

        # ------------------------------
        # 3️⃣ Hedge ratio stability
        # ------------------------------
        hr_clean = hedge_ratio_series.dropna()
        if len(hr_clean) < 20:
            result["hedge_ratio_stable"] = False
            hr_std = None
        else:
            hr_std = hr_clean.rolling(20).std().iloc[-1]
            result["hedge_ratio_stable"] = hr_std < hr_clean.std() * 0.5

        result["hedge_ratio_std"] = None if hr_std is None else float(hr_std)

        # ------------------------------
        # 4️⃣ Liquidity
        # ------------------------------
        vol_clean = volume.dropna()
        avg_vol = vol_clean.rolling(50).mean().iloc[-1]
        curr_vol = vol_clean.iloc[-1]
        result["liquidity_ok"] = curr_vol > avg_vol

        # ------------------------------
        # Final Quality
        # ------------------------------
        score = sum([
            result["stationary"],
            result["correlation_ok"],
            result["hedge_ratio_stable"],
            result["liquidity_ok"]
        ])

        if score >= 3:
            result["quality"] = "HIGH"
        elif score == 2:
            result["quality"] = "MEDIUM"
        else:
            result["quality"] = "LOW"

        return result

    except Exception as e:
        logger.exception("Signal quality computation failed")
        return {
            "quality": "LOW",
            "error": str(e)
        }
