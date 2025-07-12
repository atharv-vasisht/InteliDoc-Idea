# InteliDoc - AI Requirements & Obligations Intelligence Platform

> Turn unstructured documents into structured, actionable requirements or obligations, automatically mapped to your internal processes, policies, or backlog.

## 🚀 Features

### MVP Features
- **Document Ingestion**: Upload PDFs, DOCX, or paste text with auto OCR
- **AI-Powered Extraction**: Parse text and extract obligations/requirements as structured objects
- **Tagging & Classification**: Auto-classify by domain (Privacy, Security, Payments, etc.)
- **Mapping UI**: Link extracted items to internal controls/policies or Jira tickets
- **Semantic Search**: Full-text and semantic search across obligations/requirements
- **Reporting**: Basic gap analysis and export functionality

### Target Users
- 🎯 Compliance Managers
- 🎯 Product & Program Managers  
- 🎯 Legal/Contracts Teams
- 🎯 Business Analysts

## 🏗️ Architecture

```
[User] 
  ⬇️
[Next.js Frontend] 
  ⬇️
[FastAPI Backend]
  ⬇️
[LLM Service Layer]
  ↘️ [OpenAI GPT-4]
  ↘️ [LangChain for orchestration]
  ↘️ [Pinecone for semantic search]
  ⬇️
[PostgreSQL - obligations, mappings]
  ⬇️
[AWS S3 - documents]
```

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Headless UI + Radix UI
- **State Management**: Zustand
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI (Python)
- **AI/LLM**: Google Gemini + LangChain
- **Vector DB**: Pinecone
- **Authentication**: Supabase Auth
- **File Storage**: AWS S3

### Database
- **Primary**: PostgreSQL (Supabase)
- **Vector Search**: Pinecone

## 📦 Project Structure

```
InteliDoc/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Next.js pages
│   │   ├── hooks/          # Custom React hooks
│   │   ├── stores/         # Zustand state management
│   │   ├── types/          # TypeScript type definitions
│   │   └── utils/          # Utility functions
│   └── public/             # Static assets
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   └── requirements.txt    # Python dependencies
├── docs/                   # Documentation
└── docker-compose.yml      # Development environment
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- Docker (optional)
- Supabase account
- Google Gemini API key
- Pinecone API key
- AWS S3 bucket

### 1. Clone and Setup

```bash
git clone <repository-url>
cd InteliDoc
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Environment Configuration

Create `.env.local` in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

Create `.env` in the backend directory:
```env
DATABASE_URL=your_supabase_database_url
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_S3_BUCKET=your_s3_bucket_name
```

### 5. Run Development Servers

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

Visit `http://localhost:3000` to see the application!

## 📋 API Endpoints

### Document Management
- `POST /api/documents/upload` - Upload document
- `GET /api/documents` - List documents
- `GET /api/documents/{id}` - Get document details

### AI Extraction
- `POST /api/extract-obligations` - Extract obligations from text
- `POST /api/summarize` - Summarize document

### Obligations/Requirements
- `GET /api/obligations` - List obligations
- `PUT /api/obligations/{id}` - Update obligation
- `DELETE /api/obligations/{id}` - Delete obligation

### Mappings
- `POST /api/mappings` - Create mapping
- `GET /api/mappings` - List mappings
- `DELETE /api/mappings/{id}` - Delete mapping

### Search
- `GET /api/search` - Semantic search

### Reports
- `GET /api/reports/gap-analysis` - Generate gap analysis report

## 🎯 User Workflows

### For Compliance Teams
1. Upload new regulation (PDF)
2. Extract obligations automatically
3. Map to internal policies/controls
4. Identify unmapped obligations
5. Produce audit-ready traceability reports

### For Product Managers
1. Upload customer RFP, email, meeting notes
2. Extract feature asks / requirements
3. Tag by priority, module
4. Map to Jira backlog tickets
5. Identify gaps (unmapped requirements)

## 🔮 Roadmap

### Advanced Features
- Change detection for regulatory sites
- Automated email/slack intake
- Jira bi-directional sync
- Role-based permissions
- Audit logs and approvals
- Notifications on unmapped or stale obligations
- Integration with GRC/PLM tools

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or support, please open an issue in the GitHub repository. 