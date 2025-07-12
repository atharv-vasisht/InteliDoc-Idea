'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { 
  XMarkIcon, 
  DocumentTextIcon, 
  ArrowUpTrayIcon,
  DocumentIcon
} from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

interface DocumentUploadProps {
  onClose: () => void
}

export default function DocumentUpload({ onClose }: DocumentUploadProps) {
  const [isProcessing, setIsProcessing] = useState(false)
  const [textInput, setTextInput] = useState('')
  const [activeTab, setActiveTab] = useState<'file' | 'text'>('file')

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    setIsProcessing(true)
    
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

      // TODO: Implement file upload to backend
      toast.success(`Processing ${file.name}...`)
      
      // Simulate processing
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      toast.success('Document processed successfully!')
      onClose()
      
    } catch (error) {
      toast.error('Error processing document')
      console.error('Upload error:', error)
    } finally {
      setIsProcessing(false)
    }
  }, [onClose])

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
    
    try {
      // TODO: Implement text processing
      toast.success('Processing text...')
      
      // Simulate processing
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      toast.success('Text processed successfully!')
      onClose()
      
    } catch (error) {
      toast.error('Error processing text')
      console.error('Text processing error:', error)
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Upload Document</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6">
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
                    Supports PDF, DOCX, and TXT files (max 10MB)
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
                  Processing your {activeTab === 'file' ? 'document' : 'text'}...
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
} 