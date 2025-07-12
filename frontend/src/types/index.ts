export interface Obligation {
  id: number
  text: string
  category: Category
  priority?: Priority
  source_section?: string
  confidence_score?: number
  document_id: number
  extracted_by: number
  created_at: string
  updated_at?: string
}

export interface Document {
  id: number
  title: string
  filename: string
  file_path: string
  file_size: number
  file_type: string
  content?: string
  summary?: string
  uploaded_by: number
  created_at: string
  updated_at?: string
}

export interface Mapping {
  id: number
  obligation_id: number
  mapping_type: MappingType
  external_id: string
  external_name: string
  external_url?: string
  notes?: string
  mapped_by: number
  created_at: string
  updated_at?: string
}

export interface User {
  id: number
  email: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
  updated_at?: string
}

export enum Category {
  PRIVACY = 'privacy',
  SECURITY = 'security',
  PAYMENTS = 'payments',
  UX = 'ux',
  COMPLIANCE = 'compliance',
  LEGAL = 'legal',
  OPERATIONS = 'operations',
  OTHER = 'other'
}

export enum Priority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high'
}

export enum MappingType {
  POLICY = 'policy',
  CONTROL = 'control',
  JIRA_TICKET = 'jira_ticket',
  BACKLOG_ITEM = 'backlog_item',
  OTHER = 'other'
}

export interface ExtractionRequest {
  text: string
  document_title?: string
  document_type?: string
}

export interface ExtractedObligation {
  obligation_text: string
  category: Category
  priority?: Priority
  source_section?: string
  confidence_score?: number
}

export interface ExtractionResponse {
  obligations: ExtractedObligation[]
  total_extracted: number
  processing_time: number
}

export interface SummarizationRequest {
  text: string
  max_length?: number
}

export interface SummarizationResponse {
  summary: string
  key_points: string[]
  processing_time: number
}

export interface SearchRequest {
  query: string
  limit?: number
  category_filter?: Category
  priority_filter?: Priority
}

export interface SearchResult {
  obligation_id: number
  text: string
  category: Category
  priority?: Priority
  source_section?: string
  document_title: string
  similarity_score: number
}

export interface SearchResponse {
  results: SearchResult[]
  total_results: number
  processing_time: number
} 