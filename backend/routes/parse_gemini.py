"""
Parse endpoint with Gemini AI integration.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import os
import aiofiles
import os.path as _path
from utils.doc_parser import extract_text_from_docx, extract_all_placeholders
from utils.gemini_client import analyze_document
from utils.temp_utils import get_writable_temp_dir, generate_random_id

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
    
    # Validate file type (case-insensitive)
    if not file.filename.lower().endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")
    
    # Resolve a writable temp directory across environments (e.g., Vercel → /tmp)
    base_temp_dir = get_writable_temp_dir()
    print(f"📂 Using temp dir: {base_temp_dir}")

    # Generate unique document ID and construct file path
    document_id = generate_random_id()
    temp_file_path = _path.join(base_temp_dir, f"{document_id}_{file.filename}")
    
    try:
        # Save the uploaded file
        print(f"📝 Saving upload to {temp_file_path}")
        async with aiofiles.open(temp_file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        file_size = len(content) if content else 0
        print(f"💾 Saved file '{file.filename}' ({file_size} bytes)")

        # Extract text from document
        try:
            print("🔍 Extracting text from .docx...")
            document_text = extract_text_from_docx(temp_file_path)
            print(f"📚 Extracted document text length: {len(document_text)}")
        except Exception as e:
            # Treat invalid/corrupt .docx as a bad request
            print(f"❌ Failed to read .docx: {e}")
            import traceback as _tb
            _tb.print_exc()
            raise HTTPException(status_code=400, detail=f"Invalid .docx file: {str(e)}")
        
        # Use the improved placeholder extraction (Gemini AI only)
        print(f"📄 Calling extract_all_placeholders with {temp_file_path}")
        placeholders = await extract_all_placeholders(temp_file_path)
        print(f"✅ Got {len(placeholders)} placeholders: {placeholders}")
        
        # Analyze document content with Gemini
        print("🧠 Analyzing document with Gemini...")
        document_analysis = await analyze_document(document_text)
        print("🔎 Analysis complete")
        
        return ParseResponse(
            placeholders=placeholders,
            document_id=document_id,
            filename=file.filename,
            document_analysis=document_analysis,
            document_text=document_text
        )
        
    except HTTPException:
        # Clean up temp file on error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise
    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        import traceback as _tb
        print(f"🔥 Unexpected error in /parse-gemini: {e}")
        _tb.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
