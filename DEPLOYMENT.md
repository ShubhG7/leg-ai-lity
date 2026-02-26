# AiLaw - Deployment Guide

## 🔐 Security Setup

### Environment Variables

**IMPORTANT**: Never commit API keys to git!

#### Backend `.env` file
Create `/backend/.env` with:
```bash
GEMINI_API_KEY=your_actual_gemini_api_key
JWT_SECRET_KEY=your_secure_random_jwt_secret
```

#### Frontend `.env.local` file
Create `/frontend/.env.local` with:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Getting Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key and add it to `backend/.env`

## 🚀 Local Development

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main_simple:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Access the app at: `http://localhost:3000`

## 📦 Production Deployment

### Backend (Render/Railway/Fly.io)

1. **Set Environment Variables** in your hosting platform:
   - `GEMINI_API_KEY`
   - `JWT_SECRET_KEY`

2. **Dockerfile** (if needed):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main_simple:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. **Build command**: `pip install -r requirements.txt`
4. **Start command**: `uvicorn main_simple:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)

1. **Connect your GitHub repo** to Vercel
2. **Set Environment Variable**:
   - `NEXT_PUBLIC_API_URL=https://your-backend-url.com/api`
3. **Deploy** - Vercel will auto-deploy on push

## 🔒 Security Checklist

- [ ] `.env` files are in `.gitignore`
- [ ] API keys are stored as environment variables
- [ ] JWT secret is randomly generated and secure
- [ ] CORS is configured for your production domains
- [ ] HTTPS is enabled in production
- [ ] Rate limiting is implemented (recommended)

## 🔑 Demo Credentials

For testing/demo purposes:
- Email: `demo@lexsy.ai`
- Password: `demo123`

**Note**: Change these in production!

## 📝 Environment Variables Reference

### Required
- `GEMINI_API_KEY` - Google Gemini AI API key
- `JWT_SECRET_KEY` - Secret key for JWT token generation

### Optional
- `OPENAI_API_KEY` - OpenAI API key (if you want to use GPT instead of Gemini)

## 🌐 Production URLs

Update CORS origins in `backend/main_simple.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-production-domain.com",
        "https://*.vercel.app"
    ],
    # ...
)
```

## 🎯 API Endpoints

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/parse-gemini` - Upload and parse document
- `POST /api/chat/conversational` - Conversational AI chat
- `POST /api/fill-no-auth` - Fill document with data
- `GET /health` - Health check

## 💡 Tips

1. **Always use environment variables** for sensitive data
2. **Never commit** `.env` files to git
3. **Use `.env.example`** to document required variables
4. **Rotate API keys** periodically
5. **Monitor API usage** to control costs
6. **Enable error monitoring** in production (Sentry, etc.)

## 🆘 Troubleshooting

### "GEMINI_API_KEY not found"
- Ensure `.env` file exists in `/backend/`
- Check that the file contains `GEMINI_API_KEY=your_key`
- Restart the backend server after adding the key

### CORS Errors
- Add your frontend URL to `allow_origins` in `main_simple.py`
- Ensure backend URL is correct in frontend `.env.local`

### Authentication Fails
- Check `JWT_SECRET_KEY` is set
- Clear browser localStorage and try again

