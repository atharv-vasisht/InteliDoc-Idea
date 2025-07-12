#!/bin/bash

echo "🚀 Setting up InteliDoc - AI Requirements & Obligations Intelligence Platform"
echo "=================================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Setup Backend
echo ""
echo "📦 Setting up Backend (FastAPI)..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend dependencies installed"

# Setup Frontend
echo ""
echo "📦 Setting up Frontend (Next.js)..."
cd ../frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend dependencies installed"

# Create environment files
echo ""
echo "🔧 Creating environment files..."

# Backend .env
cd ../backend
if [ ! -f .env ]; then
    cat > .env << EOF
# Database
DATABASE_URL=postgresql://user:password@localhost/intelidoc

# Security
SECRET_KEY=your-secret-key-change-this-in-production

# Google Gemini
GEMINI_API_KEY=your-gemini-api-key-here

# Pinecone
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=your-s3-bucket-name
AWS_REGION=us-east-1
EOF
    echo "✅ Created backend/.env (please update with your actual values)"
else
    echo "⚠️  backend/.env already exists"
fi

# Frontend .env.local
cd ../frontend
if [ ! -f .env.local ]; then
    cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
    echo "✅ Created frontend/.env.local"
else
    echo "⚠️  frontend/.env.local already exists"
fi

# Return to root
cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update backend/.env with your actual API keys and database URL"
echo "2. Set up a PostgreSQL database (or use Supabase)"
echo "3. Set up AWS S3 bucket for file storage"
echo "4. Get Google Gemini API key from https://makersuite.google.com/app/apikey"
echo "5. Get Pinecone API key from https://www.pinecone.io/"
echo ""
echo "🚀 To start the application:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "🌐 Then visit http://localhost:3000"
echo ""
echo "📚 API Documentation will be available at http://localhost:8000/docs" 