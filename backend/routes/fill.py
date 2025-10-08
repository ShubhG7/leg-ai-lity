"""
Fill endpoint for generating completed documents with filled placeholders.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
import os
import uuid
from utils.doc_filler import fill_document_placeholders

router = APIRouter()

class FillRequest(BaseModel):
    document_id: str
    filename: str
    placeholder_data: Dict[str, str]

class FillResponse(BaseModel):
    download_url: str
    filled_document_id: str
    filename: str

@router.post("/fill", response_model=FillResponse)
async def fill_document(request: FillRequest):
    """
    Fill placeholders in document and return download URL.
    """
    # Find the original document
    original_file_path = f"temp/{request.document_id}_{request.filename}"
    
    if not os.path.exists(original_file_path):
        raise HTTPException(status_code=404, detail="Original document not found")
    
    # Generate new document ID for filled version
    filled_document_id = str(uuid.uuid4())
    
    # Create output filename
    name_without_ext = request.filename.rsplit('.', 1)[0]
    filled_filename = f"{filled_document_id}_{name_without_ext}_filled.docx"
    filled_file_path = f"temp/{filled_filename}"
    
    try:
        # Fill the document
        fill_document_placeholders(
            input_file_path=original_file_path,
            output_file_path=filled_file_path,
            placeholder_data=request.placeholder_data
        )
        
        # Return download URL
        download_url = f"/static/{filled_filename}"
        
        return FillResponse(
            download_url=download_url,
            filled_document_id=filled_document_id,
            filename=filled_filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filling document: {str(e)}")

@router.get("/download/{filename}")
async def download_document(filename: str):
    """
    Download a filled document.
    """
    file_path = f"temp/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@router.get("/fill/health")
async def fill_health():
    """Health check for fill service."""
    return {"status": "healthy", "service": "fill"}
