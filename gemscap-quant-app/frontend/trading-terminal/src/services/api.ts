const BASE_URL =
  import.meta.env.VITE_BACKEND_URL || "http://localhost:8000"

/* -------------------- Types -------------------- */

export interface SpreadPoint {
  ts: string
  spread: number
  zscore: number
}

export interface SpreadResponse {
  data: SpreadPoint[]
  half_life: number | null
}

export interface SignalResponse {
  quality: "HIGH" | "MEDIUM" | "LOW"
  stationary: boolean
  correlation: number | null
  hedge_ratio_stable: boolean
  liquidity_ok: boolean
}

export interface TradeAllowedResponse {
  allowed: boolean
  reason?: string
  warnings?: string[]
}

/* -------------------- Fetch Helper -------------------- */

async function safeFetch<T>(url: string, label: string): Promise<T> {
  const res = await fetch(url)

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${label} failed: ${res.status} ${text}`)
  }

  try {
    return (await res.json()) as T
  } catch {
    throw new Error(`${label} returned invalid JSON`)
  }
}

/* -------------------- API Calls -------------------- */

export function fetchSpread(
  y: string,
  x: string,
  window: number
): Promise<SpreadResponse> {
  return safeFetch(
    `${BASE_URL}/analytics/spread?symbol_y=${y}&symbol_x=${x}&window=${window}`,
    "Spread fetch"
  )
}

export function fetchSignalQuality(
  y: string,
  x: string
): Promise<SignalResponse> {
  return safeFetch(
    `${BASE_URL}/analytics/signal-quality?symbol_y=${y}&symbol_x=${x}`,
    "Signal quality fetch"
  )
}

export function fetchTradeAllowed(
  y: string,
  x: string
): Promise<TradeAllowedResponse> {
  return safeFetch(
    `${BASE_URL}/analytics/trade-allowed?symbol_y=${y}&symbol_x=${x}`,
    "Trade allowed fetch"
  )
}
