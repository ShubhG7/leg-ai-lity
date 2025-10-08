# Lexsy AI Legal Document Assistant

A production-ready full-stack web application for AI-powered legal document automation. Upload .docx legal documents, detect placeholders, and fill them through conversational AI.

## 🚀 Features

- **Smart Document Upload**: Drag-and-drop .docx file upload with progress tracking
- **AI Placeholder Detection**: Automatically detects placeholders like `[Company Name]` or `___________`
- **Conversational Filling**: Chat with AI to fill placeholders through guided questions
- **Document Generation**: Generate completed documents with original formatting preserved
- **Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS

## 🛠 Tech Stack

### Frontend
- **Next.js 14** with App Router and TypeScript
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **React Query** for API state management
- **Framer Motion** for animations
- **Zustand** for client state management

### Backend
- **FastAPI** with Python 3.11
- **python-docx** for document processing
- **OpenAI GPT-4o-mini** for AI features
- **Uvicorn** for ASGI server

## 📋 Prerequisites

- Node.js 18+ and npm/pnpm
- Python 3.11+
- OpenAI API key

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd LegAIlity
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Add your OpenAI API key to .env
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local
# Update API URL if needed (default: http://localhost:8000/api)
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` to use the application.

## 📁 Project Structure

```
LegAIlity/
├── backend/
│   ├── main.py                 # FastAPI application entry
│   ├── routes/
│   │   ├── parse.py           # Document parsing endpoint
│   │   ├── fill.py            # Document filling endpoint
│   │   └── chat.py            # Chat/conversation endpoint
│   ├── utils/
│   │   ├── doc_parser.py      # Document parsing utilities
│   │   ├── doc_filler.py      # Document filling utilities
│   │   └── openai_client.py   # OpenAI integration
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx       # Main application page
│   │   │   └── layout.tsx     # Root layout
│   │   ├── components/
│   │   │   ├── UploadZone.tsx # File upload component
│   │   │   ├── ChatUI.tsx     # Chat interface
│   │   │   └── DocumentPreview.tsx # Preview & download
│   │   └── lib/
│   │       ├── api.ts         # API client
│   │       └── store.ts       # State management
│   └── package.json
│
└── README.md
```

## 🔧 API Endpoints

### POST `/api/parse`
Upload and parse a .docx document to extract placeholders.

**Request:** Multipart form data with `file` field
**Response:**
```json
{
  "placeholders": ["Company Name", "Investor Name", "Amount"],
  "document_id": "uuid",
  "filename": "document.docx"
}
```

### POST `/api/chat/question`
Get the next question for filling placeholders.

**Request:**
```json
{
  "placeholders": ["Company Name", "Investor Name"],
  "current_data": {"Company Name": "Acme Corp"},
  "current_placeholder_index": 1
}
```

### POST `/api/chat/answer`
Submit an answer for a placeholder.

**Request:**
```json
{
  "placeholder": "Investor Name",
  "answer": "John Doe",
  "current_data": {"Company Name": "Acme Corp"}
}
```

### POST `/api/fill`
Generate filled document with all placeholder data.

**Request:**
```json
{
  "document_id": "uuid",
  "filename": "document.docx",
  "placeholder_data": {
    "Company Name": "Acme Corp",
    "Investor Name": "John Doe"
  }
}
```

## 🌟 Usage Flow

1. **Upload**: Drag and drop a .docx legal document
2. **Parse**: AI automatically detects placeholders in the document
3. **Chat**: Answer questions to fill each placeholder conversationally
4. **Generate**: Create the completed document with filled placeholders
5. **Download**: Download the finished document with original formatting

## 🔒 Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_openai_api_key_here
ENVIRONMENT=development
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 🚀 Deployment

### Backend (Render/Railway)
1. Connect your repository
2. Set environment variables
3. Deploy with `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)
1. Connect your repository
2. Set build command: `cd frontend && npm run build`
3. Set output directory: `frontend/.next`
4. Set environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

Built with ❤️ for streamlined legal document automation.
