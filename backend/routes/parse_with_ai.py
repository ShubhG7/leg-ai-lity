"""
Parse endpoint with full AI integration.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import os
import uuid
import aiofiles
from utils.doc_parser import extract_all_placeholders, extract_text_from_docx
from utils.openai_client import analyze_document
from utils.auth import get_current_user, User

router = APIRouter()

class ParseResponse(BaseModel):
    placeholders: List[str]
    document_id: str
    filename: str
    document_analysis: str

@router.post("/parse-ai", response_model=ParseResponse)
async def parse_document_with_ai(file: UploadFile = File(...)):
    """
    Parse uploaded .docx document with full AI integration (no auth for demo).
    """
    # Validate file type
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")
    
    # Generate unique document ID
    document_id = str(uuid.uuid4())
    
    # Save uploaded file temporarily
    temp_file_path = f"temp/{document_id}_{file.filename}"
    
    try:
        # Save the uploaded file
        async with aiofiles.open(temp_file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Extract placeholders with AI
        placeholders = await extract_all_placeholders(temp_file_path)
        
        # Analyze document content with AI
        document_text = extract_text_from_docx(temp_file_path)
        try:
            document_analysis = await analyze_document(document_text)
        except Exception as e:
            print(f"AI analysis failed: {e}")
            document_analysis = f"This document appears to be a legal agreement with {len(placeholders)} placeholders that need to be filled. The document contains approximately {len(document_text.split())} words."
        
        return ParseResponse(
            placeholders=placeholders,
            document_id=document_id,
            filename=file.filename,
            document_analysis=document_analysis
        )
        
    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
