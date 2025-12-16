export default function OrderStats() {
  return (
    <div className="p-4 border-b border-gray-800">
      <h3 className="font-semibold mb-2">Market Snapshot</h3>

      <div className="grid grid-cols-2 gap-2 text-sm">
        <span>Bid</span>
        <span className="text-green-400">0.02048</span>

        <span>Ask</span>
        <span className="text-red-400">0.02050</span>

        <span>Spread</span>
        <span>0.00002</span>
      </div>
    </div>
  )
}
