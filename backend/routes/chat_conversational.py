"""
Conversational chat endpoint that handles arbitrary questions and clarifications
about the document, while also guiding users through filling placeholders.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from utils.gemini_client import generate_conversational_response

router = APIRouter()

class ConversationalChatRequest(BaseModel):
    user_message: str
    placeholders: List[str]
    current_data: Dict[str, str]
    document_text: Optional[str] = None
    conversation_history: List[Dict[str, str]] = []

class ConversationalChatResponse(BaseModel):
    response: str
    suggested_field: Optional[str] = None
    should_fill_field: bool = False
    extracted_fields: Optional[Dict[str, str]] = None  # placeholder -> normalized value

@router.post("/chat/conversational", response_model=ConversationalChatResponse)
async def conversational_chat(request: ConversationalChatRequest):
    """
    Handle conversational chat that can:
    - Answer questions about the document
    - Provide clarifications
    - Guide users through filling fields
    - Handle arbitrary user messages
    """
    try:
        # Get unfilled placeholders
        unfilled = [p for p in request.placeholders if p not in request.current_data]
        filled_count = len(request.current_data)
        total_count = len(request.placeholders)
        
        response = await generate_conversational_response(
            user_message=request.user_message,
            placeholders=request.placeholders,
            current_data=request.current_data,
            unfilled_placeholders=unfilled,
            document_text=request.document_text,
            conversation_history=request.conversation_history,
            progress=(filled_count, total_count)
        )
        
        return response
        
    except Exception as e:
        print(f"Conversational chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/conversational/health")
async def conversational_chat_health():
    """Health check for conversational chat service."""
    return {"status": "healthy", "service": "conversational-chat"}

