import { useState } from 'react'

export default function ChatReorg() {
  const [input, setInput] = useState('')
  const [history, setHistory] = useState<{role: 'user'|'ai', message: string, changes?: any}[]>([])
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return
    setLoading(true)
    setHistory(h => [...h, { role: 'user', message: input }])
    try {
      const res = await fetch('http://localhost:8000/api/v1/ai/chat-reorg', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })
      const data = await res.json()
      setHistory(h => [...h, { role: 'ai', message: 'Here are the proposed changes:', changes: data.proposed_changes }])
    } catch (e) {
      setHistory(h => [...h, { role: 'ai', message: 'Error: Could not get a response from the AI.' }])
    } finally {
      setLoading(false)
      setInput('')
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto my-8">
      <h2 className="text-xl font-bold mb-4">AI Chat for Folder Reorganization</h2>
      <div className="space-y-4 mb-4 max-h-80 overflow-y-auto">
        {history.map((msg, i) => (
          <div key={i} className={msg.role === 'user' ? 'text-right' : 'text-left'}>
            <div className={msg.role === 'user' ? 'inline-block bg-blue-100 text-blue-900 px-3 py-2 rounded-lg' : 'inline-block bg-gray-100 text-gray-900 px-3 py-2 rounded-lg'}>
              {msg.message}
            </div>
            {msg.changes && (
              <pre className="bg-gray-50 border border-gray-200 rounded p-2 mt-2 text-xs overflow-x-auto">{typeof msg.changes === 'string' ? msg.changes : JSON.stringify(msg.changes, null, 2)}</pre>
            )}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="input-field flex-1"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') sendMessage() }}
          placeholder="Ask the AI to reorganize, rename, or summarize..."
          disabled={loading}
        />
        <button className="btn-primary" onClick={sendMessage} disabled={loading || !input.trim()}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
} 