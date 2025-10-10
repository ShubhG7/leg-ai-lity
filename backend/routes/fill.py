"""
Fill endpoint for generating completed documents with filled placeholders.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
import os
import os.path as _path
from utils.doc_filler import fill_document_placeholders
from utils.auth import get_current_user, User
from utils.temp_utils import get_writable_temp_dir, generate_random_id

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
async def fill_document(request: FillRequest, current_user: User = Depends(get_current_user)):
    """
    Fill placeholders in document and return download URL.
    """
    # Get writable temp directory
    base_temp_dir = get_writable_temp_dir()
    
    # Find the original document
    original_file_path = _path.join(base_temp_dir, f"{request.document_id}_{request.filename}")
    
    if not os.path.exists(original_file_path):
        raise HTTPException(status_code=404, detail="Original document not found")
    
    # Generate new document ID for filled version
    filled_document_id = generate_random_id()
    
    # Create output filename
    name_without_ext = request.filename.rsplit('.', 1)[0]
    filled_filename = f"{filled_document_id}_{name_without_ext}_filled.docx"
    filled_file_path = _path.join(base_temp_dir, filled_filename)
    
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
    base_temp_dir = get_writable_temp_dir()
    file_path = _path.join(base_temp_dir, filename)
    
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
