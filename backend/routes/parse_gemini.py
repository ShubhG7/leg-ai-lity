"""
Parse endpoint with Gemini AI integration.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import os
import uuid
import aiofiles
from utils.doc_parser import extract_text_from_docx, extract_all_placeholders
from utils.gemini_client import analyze_document

router = APIRouter()

class ParseResponse(BaseModel):
    placeholders: List[str]
    document_id: str
    filename: str
    document_analysis: str
    document_text: str

@router.post("/parse-gemini", response_model=ParseResponse)
async def parse_document_with_gemini(file: UploadFile = File(...)):
    """
    Parse uploaded .docx document with Gemini AI ONLY integration.
    """
    print("=" * 80)
    print("🚀 PARSE-GEMINI ROUTE CALLED")
    print("=" * 80)
    
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
        
        # Extract text from document
        document_text = extract_text_from_docx(temp_file_path)
        
        # Use the improved placeholder extraction (Gemini AI only)
        print(f"📄 Calling extract_all_placeholders with {temp_file_path}")
        placeholders = await extract_all_placeholders(temp_file_path)
        print(f"✅ Got {len(placeholders)} placeholders: {placeholders}")
        
        # Analyze document content with Gemini
        document_analysis = await analyze_document(document_text)
        
        return ParseResponse(
            placeholders=placeholders,
            document_id=document_id,
            filename=file.filename,
            document_analysis=document_analysis,
            document_text=document_text
        )
        
    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
