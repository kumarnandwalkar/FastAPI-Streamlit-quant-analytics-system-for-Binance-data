import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from time import sleep
import time


st.set_page_config(layout="wide")
st.header("Pairs Trading Analytics")

import os
# BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
BACKEND_URL = "http://backend:8000"

# ---------------- UI CONTROLS ---------------- #
with st.container():
    # Adjusted column ratios: 4 equal parts for controls, 3 for spacer
    # Removed col5 since Signal Quality is moving out of the header area.
    col1, col2, col3, col4, col_spacer = st.columns([1, 1, 1, 1, 3])

    with col1:
        # Removed width=200 for better scaling within the narrow column
        symbol_y = st.selectbox("Y Symbol", ["btcusdt", "ethusdt"]) # Removed width=200

    with col2:
        symbol_x = st.selectbox("X Symbol", ["ethusdt", "btcusdt"]) # Removed width=200

    with col3:
        window = st.slider("Rolling Window", 10, 200, 20) # Removed width=200

    with col4:
        refresh_interval = st.slider(
            "Auto-refresh interval (seconds)",
            min_value=1,
            max_value=30,
            value=5
        ) # Removed width=200
    
    # col_spacer is intentionally left empty

st.caption("ℹ️ Analytics will appear once sufficient live data is accumulated.")
st.markdown("---") # Visual separator

# ---------------- MAIN CONTENT LAYOUT ---------------- #
# Create a two-column structure for the main content
# col_charts_left will hold all the current analysis (Spread, Z-Score, Hedge Ratio, ADF, Alerts)
# col_metrics_right will hold Signal Quality and Strategy Simulation, stacked.
col_charts_left, col_metrics_right = st.columns([4, 1])

# --- Content for the LEFT (Charts/Analysis) ---
with col_charts_left:
    
    # ---------------- SPREAD + Z-SCORE ---------------- #
    if symbol_y == symbol_x:
        st.warning("Please select two different symbols.")
    else:
        try:
            resp = requests.get(
                f"{BACKEND_URL}/analytics/spread",
                params={
                    "symbol_y": symbol_y,
                    "symbol_x": symbol_x,
                    "window": window
                },
                timeout=5
            )
            resp.raise_for_status()
            data = resp.json()

            # Handle backend error message
            if isinstance(data, dict) and "error" in data:
                st.info(data["error"])
            else:
                df = pd.DataFrame(data["data"])

                if df.empty:
                    st.info("Waiting for more data to compute analytics...")
                else:
                    df["ts"] = pd.to_datetime(df["ts"])

                    colA, colB = st.columns(2)

                    # Spread Chart
                    with colA:
                        fig_spread = go.Figure()
                        fig_spread.add_trace(
                            go.Scatter(
                                x=df["ts"],
                                y=df["spread"],
                                name="Spread",
                                line=dict(width=2)
                            )
                        )
                        fig_spread.update_layout(
                            title="Price Spread",
                            xaxis_title="Time",
                            yaxis_title="Spread",
                            height=350
                        )
                        st.plotly_chart(fig_spread, use_container_width=True)

                    # Z-Score Chart
                    with colB:
                        fig_z = go.Figure()
                        fig_z.add_trace(
                            go.Scatter(
                                x=df["ts"],
                                y=df["zscore"],
                                name="Z-Score",
                                line=dict(width=2)
                            )
                        )
                        fig_z.add_hline(y=2, line_dash="dash", line_color="red")
                        fig_z.add_hline(y=-2, line_dash="dash", line_color="red")
                        fig_z.update_layout(
                            title="Z-Score",
                            xaxis_title="Time",
                            yaxis_title="Z",
                            height=350
                        )
                        st.plotly_chart(fig_z, use_container_width=True)
                    
                    if not df.empty:
                        csv = df.to_csv(index=False).encode("utf-8")

                        st.download_button(
                            label="📥 Download Spread Data (CSV)",
                            data=csv,
                            file_name=f"{symbol_y}_{symbol_x}_spread.csv",
                            mime="text/csv"
                        )

                    if "half_life" in data and data["half_life"] is not None:
                        st.metric("Mean Reversion Half-Life (sec)", round(data["half_life"], 2))

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching spread analytics: {e}")

    # ---------------- HEDGE RATIO ---------------- #
    st.subheader("Hedge Ratio")

    try:
        resp = requests.get(
            f"{BACKEND_URL}/analytics/hedge_ratio",
            params={"symbol_y": symbol_y, "symbol_x": symbol_x, "window": window},
            timeout=5
        )
        resp.raise_for_status()
        hr_df = pd.DataFrame(resp.json())

        if not hr_df.empty:
            hr_df["ts"] = pd.to_datetime(hr_df["ts"])
            fig_hr = go.Figure()
            fig_hr.add_trace(go.Scatter(
                x=hr_df["ts"], y=hr_df["hedge_ratio"], name="Hedge Ratio"
            ))
            fig_hr.update_layout(
                title="Hedge Ratio Over Time",
                xaxis_title="Time",
                yaxis_title="Hedge Ratio",
                height=350
            )
            st.plotly_chart(fig_hr, use_container_width=True)
        else:
            st.info("Waiting for hedge ratio data...")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching hedge ratio: {e}")

    # ---------------- ALERTS ---------------- #
    st.subheader("Alerts")

    try:
        alert_resp = requests.get(
            f"{BACKEND_URL}/alert/zscore",
            params={
                "symbol_y": symbol_y,
                "symbol_x": symbol_x,
                "window": window,
                "threshold": 2
            },
            timeout=5
        )
        alert_resp.raise_for_status()
        alert = alert_resp.json()

        if alert.get("triggered"):
            st.error(f"🚨 Z-Score Alert Triggered: {alert['value']:.2f}")
        else:
            st.success("No active alerts")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching alert data: {e}")

    # ---------------- ADF TEST ---------------- #
    st.subheader("Stationarity Test (ADF)")

    if st.button("Run ADF Test"):
        try:
            resp = requests.get(
                f"{BACKEND_URL}/analytics/adf",
                params={
                    "symbol_y": symbol_y,
                    "symbol_x": symbol_x
                },
                timeout=5
            )
            resp.raise_for_status()
            result = resp.json()

            if "p_value" in result:
                st.metric("ADF Statistic", round(result["adf_stat"], 4))
                st.metric("p-value", round(result["p_value"], 4))

                if result["p_value"] < 0.05:
                    st.success("Spread is likely mean-reverting ✅")
                else:
                    st.warning("Spread is NOT stationary ⚠️")
            else:
                st.info("Not enough data to run ADF test yet.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error running ADF test: {e}")

    # ---------------- TRADING ALLOWED ---------------- #
    # Keeping this on the left side near the core analysis
    resp = requests.get(
        f"{BACKEND_URL}/analytics/trade-allowed",
        params={"symbol_y": symbol_y, "symbol_x": symbol_x}
    )

    if resp.status_code != 200:
        st.error("Backend error checking trading status")
        data = {"allowed": False, "reason": "Backend connection failed or returned non-200 status"}
    else:
        try:
            data = resp.json()
        except ValueError:
            st.error("Invalid response from backend for trading status")
            st.stop()

    if data.get("allowed"):
        st.success("🟢 Trading Allowed")
    else:
        st.error(f"🔴 Trading Blocked: {data.get('reason', 'Unknown reason')}")
        for w in data.get("warnings", []):
            st.warning(w)

# --- Content for the RIGHT (Stacked Metrics) ---
with col_metrics_right:
    
    # ---------------- SIGNAL QUALITY ---------------- #
    st.subheader("Signal Quality")

    try:
        resp = requests.get(
            f"{BACKEND_URL}/analytics/signal-quality",
            params={"symbol_y": symbol_y, "symbol_x": symbol_x}
        )
        
        # START OF REQUESTED CHANGE 1 (Moved)
        if resp.status_code != 200:
            st.error("Backend error fetching signal quality")
            data = {} 
        else:
            try:
                data = resp.json()
            except ValueError:
                st.error("Invalid response from backend for signal quality")
                st.stop()
        # END OF REQUESTED CHANGE 1

        if data.get("quality") == "HIGH":
            st.success("✅ Signal Quality: HIGH")
        elif data.get("quality") == "MEDIUM":
            st.warning("⚠️ Signal Quality: MEDIUM")
        elif data: 
            st.error("🚫 Signal Quality: LOW")

        if data:
            corr = data.get("correlation")
            corr_str = f"{corr:.2f}" if corr is not None else "N/A"

            st.caption(
                f"""
                Stationary: {data.get('stationary')} | 
                Correlation: {corr_str} | 
                Hedge Stability: {data.get('hedge_ratio_stable')} | 
                Liquidity OK: {data.get('liquidity_ok')}
                """
            )

    except Exception as e:
        st.error(f"Signal quality unavailable: {e}")

    st.markdown("---") # Separator between stacked components

    # ---------------- STRATEGY SIMULATION ---------------- #
    st.subheader("Strategy Simulation")

    try:
        resp = requests.get(
            f"{BACKEND_URL}/analytics/backtest",
            params={
                "symbol_y": symbol_y,
                "symbol_x": symbol_x,
                "window": window
            },
            timeout=5
        )
        bt = resp.json()

        if "error" not in bt:
            # Metrics are best placed in a single column here
            st.metric("Total PnL", bt["total_pnl"])
            st.metric("Trades", bt["num_trades"])
            st.metric("Win Rate", f"{bt['win_rate'] * 100:.1f}%")
                
            if bt["num_trades"] < 5:
                st.caption(
                    "⚠️ Low trade count — results may not be statistically significant"
                )

    except:
        st.warning("Backtest unavailable")


# ---------------- AUTO REFRESH ---------------- #
time.sleep(refresh_interval)
st.rerun()