import {
  createChart,
  ColorType,
  CandlestickSeries,
} from "lightweight-charts"
import { useEffect, useRef } from "react"

export default function TradingChart() {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!ref.current) return

    const chart = createChart(ref.current, {
      height: 500,
      layout: {
        background: { type: ColorType.Solid, color: "#0b0e11" },
        textColor: "#ccc",
      },
      grid: {
        vertLines: { color: "#222" },
        horzLines: { color: "#222" },
      },
    })

    // ✅ v4+ way (THIS fixes your error)
    chart.addSeries(CandlestickSeries, {
      upColor: "#0ecb81",
      downColor: "#f6465d",
      wickUpColor: "#0ecb81",
      wickDownColor: "#f6465d",
      borderVisible: false,
    })

    return () => {
      chart.remove()
    }
  }, [])

  return <div ref={ref} className="w-full h-full" />
}
