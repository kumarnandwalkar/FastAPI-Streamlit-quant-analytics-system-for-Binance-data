import { useEffect, useState } from "react"
import Sidebar from "../components/Slidebar"
import TopBar from "../components/TopBar"
import TradingChart from "../components/TradingChart"
import AnalyticsPanel from "../components/AnalyticsPannel"
import SignalPanel from "../components/SignalPannel"
import OrderStats from "../components/OrderStats"

import {
  fetchSpread,
  fetchSignalQuality,
  fetchTradeAllowed,
} from "../services/api"

import { connectMarketWS } from "../services/websocket"

export default function Terminal() {
  const [marketStats, setMarketStats] = useState({
    price: "--",
    change: "--",
    high: "--",
    low: "--",
    volume: "--",
  })

  const [analytics, setAnalytics] = useState({
    spread: "--",
    zscore: "--",
    halfLife: "--",
  })

  const [signal, setSignal] = useState({
    allowed: false,
    reason: "Waiting for data...",
  })

  const symbolY = "btcusdt"
  const symbolX = "ethusdt"
  const window = 50

  /* -------- WebSocket: Live Market -------- */
  useEffect(() => {
    const ws = connectMarketWS(symbolY, (data) => {
      setMarketStats({
        price: data.price.toFixed(2),
        change: data.change.toFixed(2),
        high: data.high.toFixed(2),
        low: data.low.toFixed(2),
        volume: data.volume.toFixed(2),
      })
    })

    return () => ws.close()
  }, [])

  /* -------- REST Polling -------- */
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const spread = await fetchSpread(symbolY, symbolX, window)

        if (spread.data?.length) {
          const last = spread.data.at(-1)

          setAnalytics({
            spread: last.spread.toFixed(4),
            zscore: last.zscore.toFixed(2),
            halfLife: spread.half_life
              ? spread.half_life.toFixed(1)
              : "--",
          })
        }

        const signalQuality = await fetchSignalQuality(symbolY, symbolX)
        const trade = await fetchTradeAllowed(symbolY, symbolX)

        setSignal({
          allowed: trade.allowed,
          reason: trade.allowed
            ? "Trade allowed"
            : trade.reason || "Blocked by risk checks",
        })
      } catch (err) {
        console.error("Polling error:", err)
      }
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex h-screen bg-[#0b0e11] text-white">
      <Sidebar />

      <div className="flex flex-col flex-1">
        <TopBar
          price={marketStats.price}
          change={marketStats.change}
          high={marketStats.high}
          low={marketStats.low}
          volume={marketStats.volume}
        />

        <div className="flex-1">
          <TradingChart />
        </div>

        <div className="grid grid-cols-3 border-t border-gray-800">
          <AnalyticsPanel {...analytics} />
          <SignalPanel
            allowed={signal.allowed}
            reason={signal.reason}
          />
          <OrderStats />
        </div>
      </div>
    </div>
  )
}
