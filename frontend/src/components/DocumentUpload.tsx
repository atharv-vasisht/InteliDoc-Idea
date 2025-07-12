'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { 
  XMarkIcon, 
  DocumentTextIcon, 
  ArrowUpTrayIcon,
  DocumentIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

interface DocumentUploadProps {
  onClose: () => void
}

interface ExtractedObligation {
  obligation_text: string
  category: string
  priority: string
  source_section?: string
  confidence_score?: number
}

interface ExtractionResponse {
  obligations: ExtractedObligation[]
  total_extracted: number
  processing_time: number
}

interface SummarizationResponse {
  summary: string
  key_points: string[]
  processing_time: number
}

export default function DocumentUpload({ onClose }: DocumentUploadProps) {
  const [isProcessing, setIsProcessing] = useState(false)
  const [textInput, setTextInput] = useState('')
  const [activeTab, setActiveTab] = useState<'file' | 'text'>('file')
  const [results, setResults] = useState<{
    obligations: ExtractedObligation[]
    summary?: SummarizationResponse
  } | null>(null)

  const processText = async (text: string, documentTitle?: string) => {
    try {
      // Call the backend API to extract obligations
      const extractionResponse = await fetch('http://localhost:8000/api/v1/ai/extract-obligations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          document_title: documentTitle || 'Uploaded Document',
          document_type: 'general'
        }),
      })

      if (!extractionResponse.ok) {
        throw new Error(`Extraction failed: ${extractionResponse.statusText}`)
      }

      const extractionData: ExtractionResponse = await extractionResponse.json()

      // Call the backend API to generate summary
      const summaryResponse = await fetch('http://localhost:8000/api/v1/ai/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          max_length: 300
        }),
      })

      let summaryData: SummarizationResponse | undefined
      if (summaryResponse.ok) {
        summaryData = await summaryResponse.json()
      }

      setResults({
        obligations: extractionData.obligations,
        summary: summaryData
      })

      toast.success(`Successfully extracted ${extractionData.total_extracted} obligations!`)
      
    } catch (error) {
      console.error('Processing error:', error)
      toast.error('Error processing document. Please try again.')
    }
  }

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    setIsProcessing(true)
    setResults(null)
    
    try {
      const file = acceptedFiles[0]
      
      // Validate file type
      const allowedTypes = ['.pdf', '.docx', '.txt']
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
      
      if (!allowedTypes.includes(fileExtension)) {
        toast.error('Please upload a PDF, DOCX, or TXT file')
        return
      }

      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        toast.error('File size must be less than 10MB')
        return
      }

      // For now, we'll read text files directly
      // TODO: Implement PDF and DOCX processing
      if (fileExtension === '.txt') {
        const text = await file.text()
        await processText(text, file.name)
      } else {
        toast.error('PDF and DOCX processing coming soon. Please use TXT files for now.')
      }
      
    } catch (error) {
      toast.error('Error processing document')
      console.error('Upload error:', error)
    } finally {
      setIsProcessing(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false
  })

  const handleTextSubmit = async () => {
    if (!textInput.trim()) {
      toast.error('Please enter some text')
      return
    }

    setIsProcessing(true)
    setResults(null)
    
    try {
      await processText(textInput, 'Pasted Text')
    } catch (error) {
      toast.error('Error processing text')
      console.error('Text processing error:', error)
    } finally {
      setIsProcessing(false)
    }
  }

  const getCategoryColor = (category: string) => {
    const colors: { [key: string]: string } = {
      security: 'bg-red-100 text-red-800',
      privacy: 'bg-blue-100 text-blue-800',
      compliance: 'bg-yellow-100 text-yellow-800',
      legal: 'bg-purple-100 text-purple-800',
      payments: 'bg-green-100 text-green-800',
      ux: 'bg-indigo-100 text-indigo-800',
      operations: 'bg-gray-100 text-gray-800',
      other: 'bg-gray-100 text-gray-800'
    }
    return colors[category] || colors.other
  }

  const getPriorityColor = (priority: string) => {
    const colors: { [key: string]: string } = {
      high: 'bg-red-100 text-red-800',
      medium: 'bg-yellow-100 text-yellow-800',
      low: 'bg-green-100 text-green-800'
    }
    return colors[priority] || colors.medium
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Document Intelligence</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6">
          {!results ? (
            <>
              {/* Tab Navigation */}
              <div className="flex space-x-1 mb-6 bg-gray-100 p-1 rounded-lg">
                <button
                  onClick={() => setActiveTab('file')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'file'
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Upload File
                </button>
                <button
                  onClick={() => setActiveTab('text')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'text'
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Paste Text
                </button>
              </div>

              {/* File Upload Tab */}
              {activeTab === 'file' && (
                <div
                  {...getRootProps()}
                  className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                    isDragActive
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
                  }`}
                >
                  <input {...getInputProps()} />
                  <ArrowUpTrayIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                  {isDragActive ? (
                    <p className="text-primary-600 font-medium">Drop the file here...</p>
                  ) : (
                    <div>
                      <p className="text-gray-600 mb-2">
                        Drag and drop a file here, or click to select
                      </p>
                      <p className="text-sm text-gray-500">
                        Supports TXT files (PDF and DOCX coming soon)
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* Text Input Tab */}
              {activeTab === 'text' && (
                <div className="space-y-4">
                  <div>
                    <label htmlFor="text-input" className="block text-sm font-medium text-gray-700 mb-2">
                      Paste your text here
                    </label>
                    <textarea
                      id="text-input"
                      value={textInput}
                      onChange={(e) => setTextInput(e.target.value)}
                      placeholder="Paste your document text, requirements, obligations, or any unstructured content here..."
                      className="input-field h-64 resize-none"
                      disabled={isProcessing}
                    />
                  </div>
                  <div className="flex justify-end">
                    <button
                      onClick={handleTextSubmit}
                      disabled={isProcessing || !textInput.trim()}
                      className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isProcessing ? 'Processing...' : 'Process Text'}
                    </button>
                  </div>
                </div>
              )}

              {/* Processing State */}
              {isProcessing && (
                <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600 mr-3"></div>
                    <span className="text-blue-800">
                      Processing your {activeTab === 'file' ? 'document' : 'text'} with AI...
                    </span>
                  </div>
                </div>
              )}
            </>
          ) : (
            /* Results Display */
            <div className="space-y-6">
              {/* Summary Section */}
              {results.summary && (
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <DocumentTextIcon className="w-5 h-5 mr-2" />
                    Document Summary
                  </h3>
                  <p className="text-gray-700 mb-4">{results.summary.summary}</p>
                  {results.summary.key_points.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Key Points:</h4>
                      <ul className="space-y-1">
                        {results.summary.key_points.map((point, index) => (
                          <li key={index} className="flex items-start gap-2">
                            <CheckCircleIcon className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-700">{point}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Obligations Section */}
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <CheckCircleIcon className="w-5 h-5 mr-2" />
                  Extracted Obligations ({results.obligations.length})
                </h3>
                
                {results.obligations.length > 0 ? (
                  <div className="space-y-4">
                    {results.obligations.map((obligation, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg p-4">
                        <p className="text-gray-900 mb-3 font-medium">{obligation.obligation_text}</p>
                        <div className="flex flex-wrap gap-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(obligation.category)}`}>
                            {obligation.category}
                          </span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(obligation.priority)}`}>
                            {obligation.priority}
                          </span>
                          {obligation.confidence_score && (
                            <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                              {obligation.confidence_score}% confidence
                            </span>
                          )}
                        </div>
                        {obligation.source_section && (
                          <p className="text-sm text-gray-500 mt-2">
                            Source: {obligation.source_section}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <ExclamationTriangleIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">No obligations were extracted from this document.</p>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => {
                    setResults(null)
                    setTextInput('')
                  }}
                  className="btn-outline"
                >
                  Process Another Document
                </button>
                <button
                  onClick={onClose}
                  className="btn-primary"
                >
                  Close
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
} 