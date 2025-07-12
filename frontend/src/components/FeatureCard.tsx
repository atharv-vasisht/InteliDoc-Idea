import { ComponentType } from 'react'

interface FeatureCardProps {
  icon: ComponentType<{ className?: string }>
  title: string
  description: string
  color: string
}

export default function FeatureCard({ icon: Icon, title, description, color }: FeatureCardProps) {
  return (
    <div className="card text-center">
      <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${color} text-white mb-6`}>
        <Icon className="w-8 h-8" />
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-4">{title}</h3>
      <p className="text-gray-600 leading-relaxed">{description}</p>
    </div>
  )
} 