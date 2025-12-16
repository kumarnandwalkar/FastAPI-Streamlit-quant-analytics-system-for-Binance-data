@router.get("/analytics/signal-confidence")
def get_signal_confidence(symbol_y: str, symbol_x: str):
    sq = get_signal_quality(symbol_y, symbol_x)

    if not isinstance(sq, dict) or "error" in sq:
        return {"error": "Signal quality unavailable"}

    score = signal_confidence(
        stationary=sq.get("stationary"),
        correlation=sq.get("correlation"),
        hedge_stable=sq.get("hedge_ratio_stable"),
        liquidity_ok=sq.get("liquidity_ok"),
    )

    return {
        "confidence": score,
        "quality": sq.get("quality")
    }
