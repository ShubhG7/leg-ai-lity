"""
Lexsy AI Legal Document Assistant - FastAPI Backend
Main application entry point with CORS and route configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from routes import parse, fill, chat, auth
from routes import parse_gemini, parse_no_auth, fill_no_auth, chat_no_auth, chat_gemini, chat_conversational, fields

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Lexsy AI Legal Document Assistant",
    description="AI-powered legal document automation platform",
    version="1.0.0"
)

# CORS middleware for frontend integration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://*.vercel.app").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory for file processing
os.makedirs("temp", exist_ok=True)

# Mount static files for serving processed documents
app.mount("/static", StaticFiles(directory="temp"), name="static")

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(parse.router, prefix="/api", tags=["parse"])
app.include_router(parse_gemini.router, prefix="/api", tags=["parse"])
app.include_router(parse_no_auth.router, prefix="/api", tags=["parse"])
app.include_router(fill.router, prefix="/api", tags=["fill"])
app.include_router(fill_no_auth.router, prefix="/api", tags=["fill"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(chat_gemini.router, prefix="/api", tags=["chat"])
app.include_router(chat_no_auth.router, prefix="/api", tags=["chat"])
app.include_router(chat_conversational.router, prefix="/api", tags=["chat"])
app.include_router(fields.router, prefix="/api", tags=["fields"])

@app.get("/")
async def root():
    return {"message": "Lexsy AI Legal Document Assistant API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "lexsy-ai-backend"}

