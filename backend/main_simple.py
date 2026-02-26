"""
Simplified AiLaw Legal Document Assistant - FastAPI Backend
Main application entry point with auth-only functionality for testing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from routes import auth, parse_no_auth, chat_no_auth, fill_no_auth, parse_gemini, chat_gemini, chat_conversational
from utils.temp_utils import get_writable_temp_dir

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AiLaw Legal Document Assistant",
    description="AI-powered legal document automation platform",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize and mount temp directory for file processing
temp_dir = get_writable_temp_dir()
print(f"📁 Temp directory initialized: {temp_dir}")

# Mount static files for serving processed documents
app.mount("/static", StaticFiles(directory=temp_dir), name="static")

# Include routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(parse_no_auth.router, prefix="/api", tags=["parse"])
app.include_router(chat_no_auth.router, prefix="/api", tags=["chat"])
app.include_router(fill_no_auth.router, prefix="/api", tags=["fill"])
# Gemini AI-powered endpoints
app.include_router(parse_gemini.router, prefix="/api", tags=["parse-gemini"])
app.include_router(chat_gemini.router, prefix="/api", tags=["chat-gemini"])
app.include_router(chat_conversational.router, prefix="/api", tags=["chat-conversational"])

@app.get("/")
async def root():
    return {"message": "AiLaw Legal Document Assistant API - Auth Only"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "lexsy-ai-backend-auth"}
