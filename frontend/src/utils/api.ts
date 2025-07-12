import axios from 'axios'
import { 
  ExtractionRequest, 
  ExtractionResponse, 
  SummarizationRequest, 
  SummarizationResponse,
  SearchRequest,
  SearchResponse,
  Obligation,
  Document,
  Mapping
} from '@/types'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for adding auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// AI Endpoints
export const aiApi = {
  extractObligations: async (request: ExtractionRequest): Promise<ExtractionResponse> => {
    const response = await api.post('/ai/extract-obligations', request)
    return response.data
  },

  summarizeText: async (request: SummarizationRequest): Promise<SummarizationResponse> => {
    const response = await api.post('/ai/summarize', request)
    return response.data
  },
}

// Document Endpoints
export const documentApi = {
  uploadDocument: async (file: File, title: string): Promise<Document> => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('title', title)
    
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  getDocuments: async (): Promise<Document[]> => {
    const response = await api.get('/documents')
    return response.data
  },

  getDocument: async (id: number): Promise<Document> => {
    const response = await api.get(`/documents/${id}`)
    return response.data
  },
}

// Obligation Endpoints
export const obligationApi = {
  getObligations: async (documentId?: number): Promise<Obligation[]> => {
    const params = documentId ? { document_id: documentId } : {}
    const response = await api.get('/obligations', { params })
    return response.data
  },

  updateObligation: async (id: number, updates: Partial<Obligation>): Promise<Obligation> => {
    const response = await api.put(`/obligations/${id}`, updates)
    return response.data
  },

  deleteObligation: async (id: number): Promise<void> => {
    await api.delete(`/obligations/${id}`)
  },
}

// Mapping Endpoints
export const mappingApi = {
  createMapping: async (mapping: Omit<Mapping, 'id' | 'created_at' | 'updated_at'>): Promise<Mapping> => {
    const response = await api.post('/mappings', mapping)
    return response.data
  },

  getMappings: async (obligationId?: number): Promise<Mapping[]> => {
    const params = obligationId ? { obligation_id: obligationId } : {}
    const response = await api.get('/mappings', { params })
    return response.data
  },

  deleteMapping: async (id: number): Promise<void> => {
    await api.delete(`/mappings/${id}`)
  },
}

// Search Endpoints
export const searchApi = {
  searchObligations: async (request: SearchRequest): Promise<SearchResponse> => {
    const response = await api.get('/search', { params: request })
    return response.data
  },
}

// Reports Endpoints
export const reportApi = {
  generateGapAnalysis: async (documentId?: number): Promise<any> => {
    const params = documentId ? { document_id: documentId } : {}
    const response = await api.get('/reports/gap-analysis', { params })
    return response.data
  },
}

export default api 