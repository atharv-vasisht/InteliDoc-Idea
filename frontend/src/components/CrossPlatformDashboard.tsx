'use client'

import { useState, useEffect } from 'react'
import { 
  GlobeAltIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  ChartBarIcon,
  DocumentTextIcon,
  EnvelopeIcon,
  ChatBubbleLeftRightIcon,
  FolderIcon,
  UserGroupIcon,
  ShieldCheckIcon,
  CogIcon,
  ArrowPathIcon,
  EyeIcon
} from '@heroicons/react/24/outline'

interface PlatformData {
  name: string
  items_count: number
  data_types: string[]
  users: string[]
  last_activity: string
  items: any[]
}

interface GRCDiscrepancy {
  severity: string
  description: string
  platforms_involved: string[]
  compliance_framework: string
  risk_level: string
  recommended_action: string
  detected_at: string
  items_count: number
  items: any[]
}

interface CrossPlatformReport {
  report_generated_at: string
  platform_summary: Record<string, PlatformData>
  grc_discrepancies: GRCDiscrepancy[]
  risk_assessment: {
    overall_risk: string
    high_risk_discrepancies: number
    medium_risk_discrepancies: number
    low_risk_discrepancies: number
    platforms_monitored: number
    total_items_analyzed: number
  }
  intelligence_insights: string[]
}

export default function CrossPlatformDashboard() {
  const [report, setReport] = useState<CrossPlatformReport | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    fetchCrossPlatformReport()
  }, [])

  const fetchCrossPlatformReport = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:8000/api/v1/cross-platform/intelligence-report')
      if (response.ok) {
        const data = await response.json()
        setReport(data)
      }
    } catch (error) {
      console.error('Error fetching cross-platform report:', error)
    } finally {
      setLoading(false)
    }
  }

  const refreshData = async () => {
    setRefreshing(true)
    await fetchCrossPlatformReport()
    setRefreshing(false)
  }

  const getPlatformIcon = (platformName: string) => {
    const icons: Record<string, any> = {
      'Microsoft 365': GlobeAltIcon,
      'SAP ERP': CogIcon,
      'Salesforce CRM': UserGroupIcon,
      'Jira Project Management': ChartBarIcon,
      'SharePoint Document Management': FolderIcon,
      'Microsoft Teams': ChatBubbleLeftRightIcon,
      'Outlook Email': EnvelopeIcon,
      'OneDrive File Storage': DocumentTextIcon
    }
    return icons[platformName] || GlobeAltIcon
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getRiskLevelColor = (risk: string) => {
    switch (risk) {
      case 'high': return 'text-red-600'
      case 'medium': return 'text-yellow-600'
      case 'low': return 'text-green-600'
      default: return 'text-gray-600'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!report) {
    return (
      <div className="text-center py-8">
        <ExclamationTriangleIcon className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <p className="text-gray-600">Failed to load cross-platform intelligence report</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Cross-Platform Intelligence Agent</h1>
            <p className="text-gray-600 mt-1">
              Enterprise-wide AI monitoring across M365, SAP, Salesforce, and other platforms with GRC cross-validation
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              report.risk_assessment.overall_risk === 'high' ? 'text-red-600 bg-red-100' :
              report.risk_assessment.overall_risk === 'medium' ? 'text-yellow-600 bg-yellow-100' :
              'text-green-600 bg-green-100'
            }`}>
              Overall Risk: {report.risk_assessment.overall_risk.toUpperCase()}
            </div>
            <button
              onClick={refreshData}
              disabled={refreshing}
              className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50"
            >
              <ArrowPathIcon className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
              <span>{refreshing ? 'Refreshing...' : 'Refresh'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <nav className="flex space-x-8">
          {[
            { id: 'overview', name: 'Overview', icon: EyeIcon },
            { id: 'platforms', name: 'Platforms', icon: GlobeAltIcon },
            { id: 'discrepancies', name: 'GRC Discrepancies', icon: ExclamationTriangleIcon },
            { id: 'insights', name: 'Intelligence Insights', icon: ChartBarIcon }
          ].map((tab) => {
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
        {activeTab === 'overview' && <OverviewTab report={report} />}
        {activeTab === 'platforms' && <PlatformsTab report={report} getPlatformIcon={getPlatformIcon} />}
        {activeTab === 'discrepancies' && <DiscrepanciesTab report={report} getSeverityColor={getSeverityColor} getRiskLevelColor={getRiskLevelColor} />}
        {activeTab === 'insights' && <InsightsTab report={report} />}
      </div>
    </div>
  )
}

function OverviewTab({ report }: { report: CrossPlatformReport }) {
  const getRiskLevelColor = (risk: string) => {
    switch (risk) {
      case 'high': return 'text-red-600'
      case 'medium': return 'text-yellow-600'
      case 'low': return 'text-green-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Cross-Platform Intelligence Overview</h2>
      
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center">
            <GlobeAltIcon className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Platforms Monitored</p>
              <p className="text-2xl font-bold text-gray-900">{report.risk_assessment.platforms_monitored}</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center">
            <DocumentTextIcon className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Items Analyzed</p>
              <p className="text-2xl font-bold text-gray-900">{report.risk_assessment.total_items_analyzed}</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">High Risk Issues</p>
              <p className="text-2xl font-bold text-gray-900">{report.risk_assessment.high_risk_discrepancies}</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center">
            <ShieldCheckIcon className="h-8 w-8 text-purple-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Discrepancies</p>
              <p className="text-2xl font-bold text-gray-900">
                {report.risk_assessment.high_risk_discrepancies + 
                 report.risk_assessment.medium_risk_discrepancies + 
                 report.risk_assessment.low_risk_discrepancies}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Platform Activity Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-4">Platform Activity Summary</h3>
          <div className="space-y-3">
            {Object.entries(report.platform_summary).map(([key, platform]) => (
              <div key={key} className="flex items-center justify-between p-3 bg-white rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{platform.name}</p>
                  <p className="text-sm text-gray-600">{platform.items_count} items</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600">
                    {platform.last_activity ? new Date(platform.last_activity).toLocaleDateString() : 'No activity'}
                  </p>
                  <p className="text-xs text-gray-500">{platform.data_types.length} data types</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-4">Risk Assessment</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">High Risk Discrepancies</span>
              <span className="text-sm font-medium text-red-600">{report.risk_assessment.high_risk_discrepancies}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Medium Risk Discrepancies</span>
              <span className="text-sm font-medium text-yellow-600">{report.risk_assessment.medium_risk_discrepancies}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Low Risk Discrepancies</span>
              <span className="text-sm font-medium text-green-600">{report.risk_assessment.low_risk_discrepancies}</span>
            </div>
            <div className="pt-4 border-t border-gray-200">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-900">Overall Risk Level</span>
                <span className={`text-sm font-medium ${getRiskLevelColor(report.risk_assessment.overall_risk)}`}>
                  {report.risk_assessment.overall_risk.toUpperCase()}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function PlatformsTab({ report, getPlatformIcon }: { report: CrossPlatformReport, getPlatformIcon: (name: string) => any }) {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Platform Monitoring</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Object.entries(report.platform_summary).map(([key, platform]) => {
          const Icon = getPlatformIcon(platform.name)
          return (
            <div key={key} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center mb-4">
                <Icon className="h-8 w-8 text-blue-600" />
                <div className="ml-3">
                  <h3 className="font-medium text-gray-900">{platform.name}</h3>
                  <p className="text-sm text-gray-600">{platform.items_count} items</p>
                </div>
              </div>
              
              <div className="space-y-2">
                <div>
                  <p className="text-xs font-medium text-gray-600">Data Types</p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {platform.data_types.map((type, index) => (
                      <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                        {type}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div>
                  <p className="text-xs font-medium text-gray-600">Active Users</p>
                  <p className="text-sm text-gray-900">{platform.users.length} users</p>
                </div>
                
                <div>
                  <p className="text-xs font-medium text-gray-600">Last Activity</p>
                  <p className="text-sm text-gray-900">
                    {platform.last_activity ? new Date(platform.last_activity).toLocaleString() : 'No activity'}
                  </p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function DiscrepanciesTab({ report, getSeverityColor, getRiskLevelColor }: { 
  report: CrossPlatformReport, 
  getSeverityColor: (severity: string) => string,
  getRiskLevelColor: (risk: string) => string 
}) {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">GRC Cross-Validation Discrepancies</h2>
      
      {report.grc_discrepancies.length === 0 ? (
        <div className="text-center py-8">
          <CheckCircleIcon className="h-12 w-12 text-green-500 mx-auto mb-4" />
          <p className="text-gray-600">No GRC discrepancies detected across platforms</p>
        </div>
      ) : (
        <div className="space-y-6">
          {report.grc_discrepancies.map((discrepancy, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSeverityColor(discrepancy.severity)}`}>
                    {discrepancy.severity.toUpperCase()}
                  </span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskLevelColor(discrepancy.risk_level)}`}>
                    {discrepancy.risk_level.toUpperCase()} RISK
                  </span>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600">
                    {new Date(discrepancy.detected_at).toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500">{discrepancy.items_count} items involved</p>
                </div>
              </div>
              
              <div className="mb-4">
                <h3 className="font-medium text-gray-900 mb-2">Description</h3>
                <p className="text-gray-700">{discrepancy.description}</p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Platforms Involved</h4>
                  <div className="flex flex-wrap gap-2">
                    {discrepancy.platforms_involved.map((platform, idx) => (
                      <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-800 text-sm rounded">
                        {platform}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Compliance Framework</h4>
                  <p className="text-gray-700">{discrepancy.compliance_framework}</p>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Recommended Action</h4>
                <p className="text-gray-700">{discrepancy.recommended_action}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function InsightsTab({ report }: { report: CrossPlatformReport }) {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Intelligence Insights</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-4">AI-Generated Insights</h3>
          <div className="space-y-3">
            {report.intelligence_insights.map((insight, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-white rounded-lg">
                <ChartBarIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">{insight}</p>
              </div>
            ))}
          </div>
        </div>
        
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-4">Report Information</h3>
          <div className="space-y-3">
            <div>
              <p className="text-sm font-medium text-gray-600">Report Generated</p>
              <p className="text-sm text-gray-900">
                {new Date(report.report_generated_at).toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Analysis Coverage</p>
              <p className="text-sm text-gray-900">
                {report.risk_assessment.platforms_monitored} platforms, {report.risk_assessment.total_items_analyzed} items
              </p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Cross-Validation Results</p>
              <p className="text-sm text-gray-900">
                {report.grc_discrepancies.length} discrepancies detected
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 