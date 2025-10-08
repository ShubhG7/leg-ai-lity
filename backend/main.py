"""
Lexsy AI Legal Document Assistant - FastAPI Backend
Main application entry point with CORS and route configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from routes import parse, fill, chat

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Lexsy AI Legal Document Assistant",
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

# Create temp directory for file processing
os.makedirs("temp", exist_ok=True)

# Mount static files for serving processed documents
app.mount("/static", StaticFiles(directory="temp"), name="static")

# Include API routes
app.include_router(parse.router, prefix="/api", tags=["parse"])
app.include_router(fill.router, prefix="/api", tags=["fill"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Lexsy AI Legal Document Assistant API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "lexsy-ai-backend"}

