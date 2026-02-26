# 🤖 AiLaw - Legal Document Assistant

> AI-powered legal document automation platform built with Next.js, FastAPI, and Google Gemini AI

## ✨ Features

- **📄 Document Upload** - Upload `.docx` legal documents
- **🔍 Smart Placeholder Detection** - Regex + AI hybrid approach for cost optimization
- **🎯 Split-Screen Interface** - Revolutionary dual-panel design:
  - **Left Panel**: Sequential field filling with current field highlighted
  - **Right Panel**: Always-active AI chat for questions and guidance
  - **Preset Buttons**: "Explain this field" and "Give example" for instant AI help
- **💡 AI-Powered Assistance** - Google Gemini 2.5 Flash provides:
  - Document analysis and explanation
  - Field-specific explanations and examples
  - Conversational Q&A about the document
- **📝 Smart Navigation** - Jump between fields, skip, go back/forward - complete control
- **🔐 Secure Authentication** - JWT-based user authentication
- **⬇️ Document Generation** - Preview and download completed documents
- **🎨 Beautiful UI** - Modern, responsive design with Tailwind CSS

## 🏗️ Tech Stack

### Frontend
- **Next.js 14** (App Router, React 18, TypeScript)
- **Tailwind CSS** + **shadcn/ui** components
- **Framer Motion** for animations
- **Zustand** for state management
- **React Query** for async state
- **Axios** for API calls

### Backend
- **FastAPI** (Python 3.11)
- **Google Gemini 2.5 Flash** AI model
- **python-docx** for document processing
- **JWT** authentication
- **Uvicorn** ASGI server

## 🔒 Security

**IMPORTANT**: All sensitive credentials are stored in environment variables, NOT in the code.

- ✅ `.env` files are in `.gitignore` and will NOT be committed
- ✅ Demo credentials are configurable via environment variables
- ✅ See [SECURITY.md](SECURITY.md) for detailed security guidelines

### For Production:
1. Change ALL default passwords and secrets
2. Use secure, randomly generated JWT secrets
3. Implement proper database instead of in-memory storage
4. Enable HTTPS and proper authentication

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd LegAIlity
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start server
uvicorn main_simple:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on: `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env.local (optional, defaults to localhost:8000)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:3000`

### 4. Test It Out!
1. Open `http://localhost:3000`
2. Login with demo credentials:
   - Email: `demo@lexsy.ai`
   - Password: `demo123`
3. Upload a legal document (`.docx`)
4. Chat with AiLaw to fill in the fields!

## 💬 How to Use Conversational AI

### Ask Questions
```
You: "What is a valuation cap?"
AiLaw: "A valuation cap is essentially an upper limit on the price
       per share that an investor's money will convert into..."
```

### Get Clarifications
```
You: "Should I consult a lawyer?"
AiLaw: "That's an excellent question! For almost any legal document,
       it's always a good idea to consult with a qualified lawyer..."
```

### Fill Fields Naturally
- **Click on any field pill** to start filling it
- **Type naturally** in the chat
- **Ask questions anytime** - AiLaw will answer first, then guide you
- **Auto-completion** tracking with visual progress

## 📁 Project Structure

```
LegAIlity/
├── backend/
│   ├── routes/            # API endpoints
│   │   ├── auth.py        # Authentication
│   │   ├── parse_gemini.py     # Document parsing
│   │   ├── chat_conversational.py  # Conversational AI
│   │   ├── fill_no_auth.py    # Document filling
│   │   └── ...
│   ├── utils/             # Utilities
│   │   ├── gemini_client.py   # Gemini AI integration
│   │   ├── doc_parser.py      # Document processing
│   │   ├── doc_filler.py      # Placeholder replacement
│   │   └── auth.py            # Auth utilities
│   ├── main_simple.py     # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   │   ├── ChatUIConversational.tsx
│   │   │   ├── UploadZone.tsx
│   │   │   ├── DocumentPreview.tsx
│   │   │   └── ...
│   │   └── lib/           # Utilities
│   │       ├── api.ts     # API client
│   │       └── store.ts   # Zustand store
│   ├── package.json
│   └── .gitignore
├── .gitignore
├── README.md
└── DEPLOYMENT.md
```

## 🎯 Key Workflows

### Document Processing Flow
1. User uploads `.docx` file
2. Backend extracts text and placeholders (regex + AI fallback)
3. Gemini AI analyzes document and provides explanation
4. User chats with AI to understand document
5. User fills fields through conversation or clicking
6. Backend generates filled document
7. User previews and downloads

### Cost Optimization Strategy
- **Regex first**: Detects common placeholder patterns (free)
- **AI fallback**: Only uses Gemini if regex finds < 3 placeholders
- **Simple questions**: Hardcoded for common fields (name, date, amount)
- **AI questions**: Gemini only for complex legal terms

## 🔒 Security Features

- ✅ API keys stored in environment variables (never in code)
- ✅ `.env` files in `.gitignore`
- ✅ JWT-based authentication
- ✅ Password hashing (SHA256 for demo, use bcrypt in production)
- ✅ CORS configuration
- ✅ Input validation

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - Login user
- `POST /api/auth/register` - Register new user
- `GET /api/auth/me` - Get current user

### Document Processing
- `POST /api/parse-gemini` - Parse document with AI
- `POST /api/chat/conversational` - Conversational AI chat
- `POST /api/fill-no-auth` - Fill document placeholders
- `GET /health` - Health check

## 🎨 UI Components

- **UploadZone** - Drag-and-drop file upload with progress
- **ChatUIConversational** - Interactive conversational AI chat
- **DocumentPreview** - Preview and download filled documents
- **AuthForm** - Login and registration
- **AIToggle** - Switch between AI and simple modes

## 🧪 Testing

### Test the Conversational AI (Backend)
```bash
curl -X POST http://localhost:8000/api/chat/conversational \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "What is a SAFE agreement?",
    "placeholders": ["Company Name"],
    "current_data": {}
  }'
```

### Test Document Parsing
```bash
curl -X POST http://localhost:8000/api/parse-gemini \
  -F "file=@path/to/your/document.docx"
```

## 🌟 Features in Detail

### Conversational AI
- **Contextual understanding** - Knows document content and conversation history
- **Educational responses** - Explains legal terms in plain English
- **Smart question detection** - Distinguishes questions from field answers
- **Natural dialogue** - Flows like talking to a legal advisor friend
- **Flexible interaction** - Mix Q&A and field-filling naturally

### Cost Optimization
- Hybrid regex + AI approach
- Intelligent caching
- Selective AI usage for complex queries only
- Estimated cost: **~$0.01 per document** with Gemini 2.5 Flash

### User Experience
- Auto-scrolling chat
- Real-time progress tracking
- Interactive field pills
- Smooth animations
- Mobile-responsive design

## 📝 Environment Variables

### Backend Required
```bash
GEMINI_API_KEY=your_gemini_api_key_here
JWT_SECRET_KEY=your_jwt_secret_here
```

### Frontend Optional
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api  # Defaults to this
```

## 🐛 Common Issues

### "GEMINI_API_KEY not found"
→ Create `backend/.env` with your API key

### CORS errors
→ Add your frontend URL to `allow_origins` in `backend/main_simple.py`

### Build errors
→ Run `npm install` in frontend directory

## 📄 License

MIT License

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 👨‍💻 Author

Built with ❤️ for modern legal document automation

---

**Note**: This is a demo application. For production use, implement:
- Proper database (PostgreSQL/MongoDB)
- Real password hashing (bcrypt)
- Rate limiting
- Error monitoring (Sentry)
- Proper logging
- API key rotation
- User session management
