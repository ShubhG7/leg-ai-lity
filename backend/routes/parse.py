"""
Parse endpoint for extracting placeholders from uploaded documents.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import os
import aiofiles
import os.path as _path
from utils.doc_parser import extract_all_placeholders, extract_text_from_docx
from utils.gemini_client import analyze_document
from utils.auth import get_current_user, User
from utils.temp_utils import get_writable_temp_dir, generate_random_id

router = APIRouter()

class ParseResponse(BaseModel):
    placeholders: List[str]
    document_id: str
    filename: str
    document_analysis: str

@router.post("/parse", response_model=ParseResponse)
async def parse_document(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    Parse uploaded .docx document and extract placeholders.
    """
    # Validate file type
    if not file.filename.lower().endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")
    
    # Get writable temp directory and generate unique document ID
    base_temp_dir = get_writable_temp_dir()
    document_id = generate_random_id()
    
    # Save uploaded file temporarily
    temp_file_path = _path.join(base_temp_dir, f"{document_id}_{file.filename}")
    
    try:
        # Save the uploaded file
        async with aiofiles.open(temp_file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Extract placeholders
        placeholders = await extract_all_placeholders(temp_file_path)
        
        # Analyze document content
        document_text = extract_text_from_docx(temp_file_path)
        document_analysis = await analyze_document(document_text)
        
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

@router.get("/parse/health")
async def parse_health():
    """Health check for parse service."""
    return {"status": "healthy", "service": "parse"}
