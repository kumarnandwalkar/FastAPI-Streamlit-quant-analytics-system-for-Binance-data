import pandas as pd

def simulate_pairs_trade(df: pd.DataFrame):
    position = 0
    entry_price = 0
    pnl = []
    trades = []

    for i in range(1, len(df)):
        z = df.iloc[i]["zscore"]
        spread = df.iloc[i]["spread"]

        # Entry
        if position == 0:
            if z > 2:
                position = -1
                entry_price = spread
                trades.append("SHORT")
            elif z < -2:
                position = 1
                entry_price = spread
                trades.append("LONG")

        # Exit
        elif position == 1 and z >= 0:
            pnl.append(spread - entry_price)
            position = 0

        elif position == -1 and z <= 0:
            pnl.append(entry_price - spread)
            position = 0

    total_pnl = sum(pnl)

    return {
        "total_pnl": round(total_pnl, 4),
        "num_trades": len(pnl),
        "win_rate": round(sum(p > 0 for p in pnl) / len(pnl), 2) if pnl else 0
    }
