'use client'

import { useState, useEffect } from 'react'
import { 
  ChartBarIcon, 
  DocumentTextIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  UserGroupIcon,
  ShieldCheckIcon,
  CogIcon
} from '@heroicons/react/24/outline'

interface DashboardStats {
  totalObligations: number
  mappedObligations: number
  unmappedObligations: number
  highPriorityObligations: number
  complianceGaps: number
  recentDocuments: number
  activeProjects: number
  riskLevel: 'low' | 'medium' | 'high' | 'critical'
}

interface ComplianceFramework {
  name: string
  coverage: number
  gaps: number
  status: 'compliant' | 'partial' | 'non-compliant'
}

interface RecentActivity {
  id: string
  type: 'document_upload' | 'obligation_extracted' | 'mapping_created' | 'compliance_alert'
  title: string
  description: string
  timestamp: string
  priority?: 'low' | 'medium' | 'high'
}

export default function EnterpriseDashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalObligations: 0,
    mappedObligations: 0,
    unmappedObligations: 0,
    highPriorityObligations: 0,
    complianceGaps: 0,
    recentDocuments: 0,
    activeProjects: 0,
    riskLevel: 'medium'
  })

  const [complianceFrameworks, setComplianceFrameworks] = useState<ComplianceFramework[]>([
    { name: 'SOC2', coverage: 85, gaps: 3, status: 'partial' },
    { name: 'GDPR', coverage: 92, gaps: 1, status: 'compliant' },
    { name: 'ISO27001', coverage: 78, gaps: 5, status: 'partial' },
    { name: 'HIPAA', coverage: 95, gaps: 0, status: 'compliant' }
  ])

  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch dashboard statistics
      const statsResponse = await fetch('http://localhost:8000/api/v1/reports/dashboard-stats')
      if (statsResponse.ok) {
        const statsData = await statsResponse.json()
        setStats(statsData)
      }

      // Fetch recent activity
      const activityResponse = await fetch('http://localhost:8000/api/v1/reports/recent-activity')
      if (activityResponse.ok) {
        const activityData = await activityResponse.json()
        setRecentActivity(activityData)
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-600 bg-green-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'high': return 'text-orange-600 bg-orange-100'
      case 'critical': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getComplianceStatusColor = (status: string) => {
    switch (status) {
      case 'compliant': return 'text-green-600'
      case 'partial': return 'text-yellow-600'
      case 'non-compliant': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'document_upload': return DocumentTextIcon
      case 'obligation_extracted': return ChartBarIcon
      case 'mapping_created': return CheckCircleIcon
      case 'compliance_alert': return ExclamationTriangleIcon
      default: return CogIcon
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Enterprise Dashboard</h1>
            <p className="text-gray-600 mt-1">Comprehensive view for PMO, GRC, and Product Management</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskLevelColor(stats.riskLevel)}`}>
              Risk Level: {stats.riskLevel.toUpperCase()}
            </div>
            <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors">
              Generate Report
            </button>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <DocumentTextIcon className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Obligations</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalObligations}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckCircleIcon className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Mapped</p>
              <p className="text-2xl font-bold text-gray-900">{stats.mappedObligations}</p>
              <p className="text-sm text-gray-500">
                {stats.totalObligations > 0 ? Math.round((stats.mappedObligations / stats.totalObligations) * 100) : 0}% coverage
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <ExclamationTriangleIcon className="h-8 w-8 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">High Priority</p>
              <p className="text-2xl font-bold text-gray-900">{stats.highPriorityObligations}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <ShieldCheckIcon className="h-8 w-8 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Compliance Gaps</p>
              <p className="text-2xl font-bold text-gray-900">{stats.complianceGaps}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Compliance Frameworks and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Compliance Frameworks */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Compliance Frameworks</h3>
          <div className="space-y-4">
            {complianceFrameworks.map((framework, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${
                    framework.status === 'compliant' ? 'bg-green-500' :
                    framework.status === 'partial' ? 'bg-yellow-500' : 'bg-red-500'
                  }`}></div>
                  <div>
                    <p className="font-medium text-gray-900">{framework.name}</p>
                    <p className="text-sm text-gray-600">{framework.gaps} gaps identified</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`font-semibold ${getComplianceStatusColor(framework.status)}`}>
                    {framework.coverage}%
                  </p>
                  <p className="text-sm text-gray-600 capitalize">{framework.status}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <div className="space-y-4">
            {recentActivity.length > 0 ? (
              recentActivity.map((activity, index) => {
                const Icon = getActivityIcon(activity.type)
                return (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                    <Icon className="h-5 w-5 text-gray-600 mt-0.5" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">{activity.title}</p>
                      <p className="text-sm text-gray-600">{activity.description}</p>
                      <p className="text-xs text-gray-500 mt-1">{activity.timestamp}</p>
                    </div>
                    {activity.priority && (
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        activity.priority === 'high' ? 'bg-red-100 text-red-800' :
                        activity.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {activity.priority}
                      </span>
                    )}
                  </div>
                )
              })
            ) : (
              <div className="text-center py-8 text-gray-500">
                <ClockIcon className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No recent activity</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <DocumentTextIcon className="h-6 w-6 text-blue-600 mr-3" />
            <span className="font-medium">Upload Document</span>
          </button>
          <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <ChartBarIcon className="h-6 w-6 text-green-600 mr-3" />
            <span className="font-medium">Run Gap Analysis</span>
          </button>
          <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <UserGroupIcon className="h-6 w-6 text-purple-600 mr-3" />
            <span className="font-medium">Assign Tasks</span>
          </button>
        </div>
      </div>
    </div>
  )
} 