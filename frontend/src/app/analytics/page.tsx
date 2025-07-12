import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts'

const sampleProjectData = [
  { name: 'Completed', value: 60 },
  { name: 'In Progress', value: 30 },
  { name: 'Blocked', value: 10 },
]
const COLORS = ['#2563eb', '#fbbf24', '#ef4444']

const teamProgress = [
  { name: 'Alice', uploads: 12, completed: 10 },
  { name: 'Bob', uploads: 8, completed: 7 },
  { name: 'Carol', uploads: 15, completed: 12 },
  { name: 'Dave', uploads: 5, completed: 3 },
]

export default function AnalyticsPage() {
  return (
    <div className="max-w-3xl mx-auto py-20 px-4">
      <h1 className="text-5xl font-extrabold mb-6 text-primary-700">Analytics</h1>
      <p className="text-xl text-gray-700 mb-8">
        Analytics features coming soon.
      </p>
    </div>
  )
} 