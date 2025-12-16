export default function Sidebar() {
  return (
    <div className="w-14 bg-[#0b0e11] border-r border-gray-800 flex flex-col items-center py-4 space-y-6">
      <button aria-label="Home">🏠</button>
      <button aria-label="Markets">📈</button>
      <button aria-label="Analytics">📊</button>
      <button aria-label="Signals">🧠</button>
      <button aria-label="Settings">⚙️</button>
    </div>
  )
}
