def trade_allowed(signal_quality):
    issues = []

    if not signal_quality.get("stationary"):
        issues.append("Not mean-reverting")

    if signal_quality.get("correlation", 0) < 0.5:
        issues.append("Weak relationship")

    if not signal_quality.get("hedge_ratio_stable"):
        issues.append("Unstable relationship")

    if not signal_quality.get("liquidity_ok"):
        issues.append("Low liquidity")

    if len(issues) == 0:
        status = "TRADEABLE"
        color = "GREEN"
    elif len(issues) <= 2:
        status = "CAUTION"
        color = "YELLOW"
    else:
        status = "NO_TRADE"
        color = "RED"

    return {
        "status": status,
        "color": color,
        "issues": issues
    }
