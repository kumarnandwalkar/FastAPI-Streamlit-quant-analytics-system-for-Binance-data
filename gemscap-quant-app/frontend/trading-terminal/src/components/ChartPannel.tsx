import { useEffect, useRef } from "react"

interface TradingViewWidget {
  widget: (config: Record<string, unknown>) => void
}

declare global {
  interface Window {
    TradingView?: TradingViewWidget
  }
}

export default function ChartPanel() {
  const initialized = useRef(false)

  useEffect(() => {
    if (!window.TradingView || initialized.current) return

    initialized.current = true

    window.TradingView.widget({
      symbol: "BINANCE:ETHBTC",
      interval: "60",
      container_id: "tv_chart",
      theme: "dark",
      style: "1",
      locale: "en",
      autosize: true,
      allow_symbol_change: true,
    })
  }, [])

  return <div id="tv_chart" className="h-full w-full" />
}
