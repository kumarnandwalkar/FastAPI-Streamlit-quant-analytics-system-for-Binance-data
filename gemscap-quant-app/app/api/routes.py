from fastapi import APIRouter
import pandas as pd
import logging

from app.ingestion.binance_ws import TICK_BUFFER
from app.analytics.resample import resample_ticks
from app.analytics.regression import hedge_ratio
from app.analytics.spread import compute_spread
from app.analytics.zscore import zscore
from app.analytics.alerts import check_zscore_alert
from app.analytics.adf import adf_test
from app.analytics.regression import rolling_hedge_ratio
from app.analytics.half_life import half_life
from app.cache.redis_client import get_cache, set_cache

logger = logging.getLogger("routes")
router = APIRouter()


# -------------------------------
# Z-SCORE ALERT ENDPOINT
# -------------------------------
@router.get("/alert/zscore")
def zscore_alert(
    symbol_y: str,
    symbol_x: str,
    window: int = 50,
    threshold: float = 2.0
):
    try:
        y_raw = pd.DataFrame(list(TICK_BUFFER[symbol_y]))
        x_raw = pd.DataFrame(list(TICK_BUFFER[symbol_x]))

        if y_raw.empty or x_raw.empty:
            return {"error": "Not enough data yet"}

        y = resample_ticks(y_raw, "1s")
        x = resample_ticks(x_raw, "1s")

        common_index = y.index.intersection(x.index)
        y = y.loc[common_index]
        x = x.loc[common_index]

        if len(y) < window:
            return {"error": "Waiting for more data"}

        beta = hedge_ratio(x, y)
        spread = compute_spread(y, x, beta)
        z = zscore(spread, window)

        return check_zscore_alert(z, threshold)
    except Exception as e:
        logger.error(f"Error in zscore_alert: {str(e)}", exc_info=True)
        return {"error": str(e)}


# -------------------------------
# SPREAD + Z-SCORE ANALYTICS
# -------------------------------
@router.get("/analytics/spread")
def spread_analytics(
    symbol_y: str,
    symbol_x: str,
    window: int = 50
):
    try:
        cache_key = f"{symbol_y}:{symbol_x}:{window}"
        cached = get_cache(cache_key)
        
        if cached:
            return cached
        
        y_raw = pd.DataFrame(list(TICK_BUFFER[symbol_y]))
        x_raw = pd.DataFrame(list(TICK_BUFFER[symbol_x]))

        if y_raw.empty or x_raw.empty:
            return {"error": "Not enough data yet"}

        y = resample_ticks(y_raw, "1s")
        x = resample_ticks(x_raw, "1s")

        common_index = y.index.intersection(x.index)
        y = y.loc[common_index]
        x = x.loc[common_index]

        if len(y) < window:
            return {"error": "Waiting for more data"}

        beta = hedge_ratio(x, y)
        spread = compute_spread(y, x, beta)
        z = zscore(spread, window)

        # Align spread and zscore by their common index
        common_idx = spread.index.intersection(z.index)
        spread_aligned = spread.loc[common_idx]
        z_aligned = z.loc[common_idx]

        result = pd.DataFrame({
            "ts": spread_aligned.index.astype(str),
            "spread": spread_aligned.values,
            "zscore": z_aligned.values
        })

        hl = half_life(spread)

        response = {
            "data": result.tail(300).to_dict("records"),
            "half_life": float(hl) if hl is not None else None
        }
        
        set_cache(cache_key, response)
        return response
    except Exception as e:
        logger.error(f"Error in spread_analytics: {str(e)}", exc_info=True)
        return {"error": str(e)}


# -------------------------------
# ADF TEST ENDPOINT
# -------------------------------
@router.get("/analytics/adf")
def adf(symbol_y: str, symbol_x: str):
    try:
        y_raw = pd.DataFrame(list(TICK_BUFFER[symbol_y]))
        x_raw = pd.DataFrame(list(TICK_BUFFER[symbol_x]))

        if y_raw.empty or x_raw.empty:
            return {"error": "Not enough data yet"}

        y = resample_ticks(y_raw, "1s")
        x = resample_ticks(x_raw, "1s")

        common_index = y.index.intersection(x.index)
        y = y.loc[common_index]
        x = x.loc[common_index]

        if len(y) < 50:
            return {"error": "Waiting for more data"}

        beta = hedge_ratio(x, y)
        spread = compute_spread(y, x, beta)

        return adf_test(spread)
    except Exception as e:
        logger.error(f"Error in adf: {str(e)}", exc_info=True)
        return {"error": str(e)}


@router.get("/analytics/hedge_ratio")
def hedge_ratio_rolling(symbol_y: str, symbol_x: str, window: int = 50):
    try:
        y_raw = pd.DataFrame(list(TICK_BUFFER[symbol_y]))
        x_raw = pd.DataFrame(list(TICK_BUFFER[symbol_x]))

        y = resample_ticks(y_raw, "1s")
        x = resample_ticks(x_raw, "1s")

        common = y.index.intersection(x.index)
        y, x = y.loc[common], x.loc[common]

        hr = rolling_hedge_ratio(x, y, window)

        return pd.DataFrame({
            "ts": hr.index.astype(str),
            "hedge_ratio": hr.values
        }).dropna().tail(300).to_dict("records")
    except Exception as e:
        logger.error(f"Error in hedge_ratio_rolling: {str(e)}", exc_info=True)
        return {"error": str(e)}