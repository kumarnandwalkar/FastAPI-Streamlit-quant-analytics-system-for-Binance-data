export default function AnalyticsPanel({
  spread,
  zscore,
  halfLife,
}: {
  spread: string
  zscore: string
  halfLife: string
}) {
  return (
    <div className="p-3 border-r border-gray-800">
      <h3 className="text-sm text-gray-400 mb-2">Analytics</h3>
      <p>Spread: {spread}</p>
      <p>Z-Score: {zscore}</p>
      <p>Half Life: {halfLife}</p>
    </div>
  )
}
