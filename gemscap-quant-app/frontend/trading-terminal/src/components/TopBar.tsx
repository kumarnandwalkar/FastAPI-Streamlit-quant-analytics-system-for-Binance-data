type Props = {
  price: string
  change: string
  high: string
  low: string
  volume: string
}

export default function TopBar({
  price,
  change,
  high,
  low,
  volume,
}: Props) {
  const changeNum = Number(change) || 0

  return (
    <div className="flex items-center gap-8 px-6 py-3 bg-[#0b0e11] border-b border-gray-800">
      <span className="font-semibold text-lg">BTC / ETH</span>

      <span>Last: {price}</span>

      <span className={changeNum >= 0 ? "text-green-400" : "text-red-400"}>
        24h: {change}%
      </span>

      <span>High: {high}</span>
      <span>Low: {low}</span>
      <span>Vol: {volume}</span>
    </div>
  )
}
