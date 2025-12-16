type Props = {
  allowed: boolean
  reason: string
}

export default function SignalPanel({ allowed, reason }: Props) {
  return (
    <div className="p-4 border-r border-gray-800">
      <h3 className="font-semibold mb-2">Trade Signal</h3>

      {allowed ? (
        <div className="text-green-400 font-medium">
          🟢 Trade Allowed
        </div>
      ) : (
        <div className="text-red-400 font-medium">
          🔴 Trade Blocked
          <div className="text-xs text-gray-400 mt-1">
            {reason}
          </div>
        </div>
      )}
    </div>
  )
}
