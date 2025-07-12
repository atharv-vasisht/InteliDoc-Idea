'use client'

import { useEffect, useState } from 'react'
import { 
  DocumentTextIcon, 
  MagnifyingGlassIcon, 
  ChartBarIcon,
  ArrowRightIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'
import DocumentUpload from '@/components/DocumentUpload'
import FeatureCard from '@/components/FeatureCard'
import ChatReorg from '@/components/ChatReorg'

export default function HomePage() {
  const [showUpload, setShowUpload] = useState(false)
  const [unstaged, setUnstaged] = useState<any>(null)
  const [loadingUnstaged, setLoadingUnstaged] = useState(false)

  const fetchUnstaged = async () => {
    setLoadingUnstaged(true)
    try {
      const res = await fetch('http://localhost:8000/api/v1/ai/propose-reorg', { method: 'POST' })
      const data = await res.json()
      setUnstaged(data)
    } catch (e) {
      setUnstaged({ error: 'Failed to fetch unstaged changes.' })
    } finally {
      setLoadingUnstaged(false)
    }
  }

  const features = [
    {
      icon: DocumentTextIcon,
      title: 'AI-Powered Extraction',
      description: 'Automatically extract obligations and requirements from PDFs, DOCX files, or pasted text using advanced AI.',
      color: 'bg-blue-500'
    },
    {
      icon: MagnifyingGlassIcon,
      title: 'Smart Classification',
      description: 'Intelligent categorization by domain (Privacy, Security, Payments, UX, Compliance, Legal, Operations).',
      color: 'bg-green-500'
    },
    {
      icon: ChartBarIcon,
      title: 'Mapping & Reporting',
      description: 'Link extracted items to internal controls, policies, or Jira tickets. Generate audit-ready reports.',
      color: 'bg-purple-500'
    }
  ]

  const useCases = [
    {
      title: 'For Compliance Teams',
      description: 'Map regulatory requirements to policies in minutes',
      items: [
        'Upload new regulations (PDF)',
        'Extract obligations automatically',
        'Map to internal policies/controls',
        'Identify unmapped obligations',
        'Produce audit-ready traceability reports'
      ]
    },
    {
      title: 'For Product Managers',
      description: 'Turn intake chaos into structured requirements',
      items: [
        'Upload customer RFP, email, meeting notes',
        'Extract feature asks / requirements',
        'Tag by priority, module',
        'Map to Jira backlog tickets',
        'Identify gaps (unmapped requirements)'
      ]
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              AI Requirements & Obligations Intelligence
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100 max-w-3xl mx-auto">
              Turn unstructured documents into structured, actionable requirements or obligations, 
              automatically mapped to your internal processes, policies, or backlog.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => setShowUpload(true)}
                className="btn-primary text-lg px-8 py-3 flex items-center justify-center gap-2"
              >
                Try It Now
                <ArrowRightIcon className="w-5 h-5" />
              </button>
              <button className="btn-outline text-lg px-8 py-3 bg-white/10 border-white/20 text-white hover:bg-white/20">
                Learn More
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Unstaged Changes Section */}
      <div className="py-12 bg-white border-t border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-900">Unstaged AI-Proposed Changes</h2>
            <button onClick={fetchUnstaged} className="btn-primary" disabled={loadingUnstaged}>
              {loadingUnstaged ? 'Loading...' : 'Fetch Unstaged Changes'}
            </button>
          </div>
          {unstaged ? (
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              {unstaged.error ? (
                <div className="text-red-600">{unstaged.error}</div>
              ) : (
                <>
                  <div className="mb-4">
                    <h3 className="font-semibold mb-1">Current Folder Tree:</h3>
                    <pre className="bg-white p-2 rounded text-xs overflow-x-auto border border-gray-100">{JSON.stringify(unstaged.folder_tree, null, 2)}</pre>
                  </div>
                  <div className="mb-4">
                    <h3 className="font-semibold mb-1">File Summaries:</h3>
                    <pre className="bg-white p-2 rounded text-xs overflow-x-auto border border-gray-100">{JSON.stringify(unstaged.file_summaries, null, 2)}</pre>
                  </div>
                  <div>
                    <h3 className="font-semibold mb-1">Proposed Changes:</h3>
                    <pre className="bg-white p-2 rounded text-xs overflow-x-auto border border-gray-100">{typeof unstaged.proposed_changes === 'string' ? unstaged.proposed_changes : JSON.stringify(unstaged.proposed_changes, null, 2)}</pre>
                  </div>
                </>
              )}
            </div>
          ) : (
            <div className="text-gray-500">No unstaged changes loaded yet.</div>
          )}
        </div>
      </div>

      {/* Chat Reorg Section */}
      <ChatReorg />

      {/* Features Section */}
      <div className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Every Team
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Whether you're in compliance, product management, legal, or operations, 
              InteliDoc helps you extract and organize requirements efficiently.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
            ))}
          </div>
        </div>
      </div>

      {/* Use Cases Section */}
      <div className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Designed for Your Workflow
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Tailored solutions for different teams and use cases
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {useCases.map((useCase, index) => (
              <div key={index} className="card">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                  {useCase.title}
                </h3>
                <p className="text-gray-600 mb-6">
                  {useCase.description}
                </p>
                <ul className="space-y-3">
                  {useCase.items.map((item, itemIndex) => (
                    <li key={itemIndex} className="flex items-start gap-3">
                      <CheckCircleIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-24 bg-primary-600 text-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Transform Your Document Processing?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Start extracting obligations and requirements with AI today. 
            No setup required, just upload your documents and see the magic happen.
          </p>
          <button
            onClick={() => setShowUpload(true)}
            className="btn-primary text-lg px-8 py-3 bg-white text-primary-600 hover:bg-gray-100"
          >
            Get Started Now
          </button>
        </div>
      </div>

      {/* Document Upload Modal */}
      {showUpload && (
        <DocumentUpload onClose={() => setShowUpload(false)} />
      )}
    </div>
  )
} 