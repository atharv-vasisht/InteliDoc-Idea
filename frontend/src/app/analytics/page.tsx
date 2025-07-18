'use client'

import { useState } from 'react'
import EnterpriseDashboard from '@/components/EnterpriseDashboard'
import { 
  ChartBarIcon, 
  DocumentTextIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  UserGroupIcon,
  ShieldCheckIcon,
  CogIcon,
  TableCellsIcon,
  ChartPieIcon,
  DocumentMagnifyingGlassIcon
} from '@heroicons/react/24/outline'

export default function AnalyticsPage() {
  const [activeTab, setActiveTab] = useState('dashboard')

  const tabs = [
    { id: 'dashboard', name: 'Dashboard', icon: ChartBarIcon },
    { id: 'compliance', name: 'Compliance', icon: ShieldCheckIcon },
    { id: 'obligations', name: 'Obligations', icon: DocumentTextIcon },
    { id: 'mappings', name: 'Mappings', icon: CheckCircleIcon },
    { id: 'reports', name: 'Reports', icon: DocumentMagnifyingGlassIcon }
  ]

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <EnterpriseDashboard />
      case 'compliance':
        return <ComplianceView />
      case 'obligations':
        return <ObligationsView />
      case 'mappings':
        return <MappingsView />
      case 'reports':
        return <ReportsView />
      default:
        return <EnterpriseDashboard />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Analytics & Intelligence</h1>
          <p className="text-gray-600 mt-2">
            Comprehensive analytics for enterprise document management, compliance tracking, and requirement traceability
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="mb-8">
          <nav className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{tab.name}</span>
                </button>
              )
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          {renderTabContent()}
        </div>
      </div>
    </div>
  )
}

// Placeholder components for other tabs
function ComplianceView() {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Compliance Analytics</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-2">Framework Coverage</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">SOC2</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '85%' }}></div>
                </div>
                <span className="text-sm font-medium">85%</span>
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">GDPR</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '92%' }}></div>
                </div>
                <span className="text-sm font-medium">92%</span>
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">ISO27001</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 bg-gray-200 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '78%' }}></div>
                </div>
                <span className="text-sm font-medium">78%</span>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-2">Risk Assessment</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Critical Risks</span>
              <span className="text-sm font-medium text-red-600">3</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">High Risks</span>
              <span className="text-sm font-medium text-orange-600">7</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Medium Risks</span>
              <span className="text-sm font-medium text-yellow-600">12</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Low Risks</span>
              <span className="text-sm font-medium text-green-600">25</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function ObligationsView() {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Obligations Analytics</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-2">By Category</h3>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Security</span>
              <span className="text-sm font-medium">45</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Privacy</span>
              <span className="text-sm font-medium">32</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Compliance</span>
              <span className="text-sm font-medium">28</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Legal</span>
              <span className="text-sm font-medium">19</span>
            </div>
          </div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-2">By Priority</h3>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">High</span>
              <span className="text-sm font-medium text-red-600">23</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Medium</span>
              <span className="text-sm font-medium text-yellow-600">67</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Low</span>
              <span className="text-sm font-medium text-green-600">34</span>
            </div>
          </div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-2">By Status</h3>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Mapped</span>
              <span className="text-sm font-medium text-green-600">89</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Unmapped</span>
              <span className="text-sm font-medium text-red-600">35</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">In Progress</span>
              <span className="text-sm font-medium text-blue-600">12</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function MappingsView() {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Mapping Analytics</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-2">Mapping Coverage</h3>
          <div className="text-center py-8">
            <div className="relative inline-flex items-center justify-center w-32 h-32">
              <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 120 120">
                <circle
                  cx="60"
                  cy="60"
                  r="54"
                  fill="none"
                  stroke="#e5e7eb"
                  strokeWidth="12"
                />
                <circle
                  cx="60"
                  cy="60"
                  r="54"
                  fill="none"
                  stroke="#10b981"
                  strokeWidth="12"
                  strokeDasharray="339.292"
                  strokeDashoffset="33.9292"
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute">
                <span className="text-2xl font-bold text-gray-900">90%</span>
                <p className="text-sm text-gray-600">Coverage</p>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-2">Mapping Types</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Internal Controls</span>
              <span className="text-sm font-medium">67</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Jira Tickets</span>
              <span className="text-sm font-medium">45</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Policies</span>
              <span className="text-sm font-medium">23</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Procedures</span>
              <span className="text-sm font-medium">18</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function ReportsView() {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Reports & Exports</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-4">Generate Reports</h3>
          <div className="space-y-3">
            <button className="w-full text-left p-3 bg-white rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Gap Analysis Report</p>
                  <p className="text-sm text-gray-600">Comprehensive compliance gap analysis</p>
                </div>
                <DocumentMagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
            </button>
            <button className="w-full text-left p-3 bg-white rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Obligation Summary</p>
                  <p className="text-sm text-gray-600">All obligations with mapping status</p>
                </div>
                <TableCellsIcon className="h-5 w-5 text-gray-400" />
              </div>
            </button>
            <button className="w-full text-left p-3 bg-white rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Risk Assessment</p>
                  <p className="text-sm text-gray-600">Detailed risk analysis and recommendations</p>
                </div>
                <ExclamationTriangleIcon className="h-5 w-5 text-gray-400" />
              </div>
            </button>
          </div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-4">Recent Reports</h3>
          <div className="space-y-3">
            <div className="p-3 bg-white rounded-lg border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Q1 Compliance Report</p>
                  <p className="text-sm text-gray-600">Generated 2 days ago</p>
                </div>
                <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                  Download
                </button>
              </div>
            </div>
            <div className="p-3 bg-white rounded-lg border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Security Obligations Audit</p>
                  <p className="text-sm text-gray-600">Generated 1 week ago</p>
                </div>
                <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                  Download
                </button>
              </div>
            </div>
            <div className="p-3 bg-white rounded-lg border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">GDPR Compliance Status</p>
                  <p className="text-sm text-gray-600">Generated 2 weeks ago</p>
                </div>
                <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                  Download
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 