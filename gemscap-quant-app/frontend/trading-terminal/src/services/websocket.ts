export interface TickerMessage {
  price: number
  high: number
  low: number
  volume: number
  change: number
}

const WS_BASE =
  import.meta.env.VITE_WS_URL || "ws://localhost:8000"

interface WSOptions {
  reconnect?: boolean
  reconnectDelay?: number
}

export function connectMarketWS(
  symbol: string,
  onMessage: (data: TickerMessage) => void,
  options: WSOptions = { reconnect: true, reconnectDelay: 3000 }
): WebSocket {
  let ws: WebSocket

  const connect = () => {
    ws = new WebSocket(`${WS_BASE}/ws/ticks/${symbol}`)

    ws.onopen = () => {
      console.log(`[WS] Connected: ${symbol}`)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as TickerMessage
        onMessage(data)
      } catch (err) {
        console.error("[WS] Invalid message", err)
      }
    }

    ws.onerror = (err) => {
      console.error("[WS] Error", err)
    }

    ws.onclose = () => {
      console.warn(`[WS] Disconnected: ${symbol}`)
      if (options.reconnect) {
        setTimeout(connect, options.reconnectDelay)
      }
    }
  }

  connect()
  return ws!
}
