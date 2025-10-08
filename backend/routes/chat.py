"""
Chat endpoint for conversational placeholder filling.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from utils.openai_client import generate_chat_question

router = APIRouter()

class ChatRequest(BaseModel):
    placeholders: List[str]
    current_data: Dict[str, str] = {}
    current_placeholder_index: Optional[int] = None

class ChatResponse(BaseModel):
    question: str
    current_placeholder: str
    placeholder_index: int
    total_placeholders: int
    is_complete: bool

@router.post("/chat/question", response_model=ChatResponse)
async def get_next_question(request: ChatRequest):
    """
    Get the next question for filling placeholders conversationally.
    """
    if not request.placeholders:
        raise HTTPException(status_code=400, detail="No placeholders provided")
    
    # Determine current placeholder index
    if request.current_placeholder_index is None:
        # Start with first unfilled placeholder
        current_index = 0
        for i, placeholder in enumerate(request.placeholders):
            if placeholder not in request.current_data:
                current_index = i
                break
    else:
        current_index = request.current_placeholder_index
    
    # Check if all placeholders are filled
    unfilled_placeholders = [p for p in request.placeholders if p not in request.current_data]
    
    if not unfilled_placeholders:
        return ChatResponse(
            question="All placeholders have been filled! You can now generate your document.",
            current_placeholder="",
            placeholder_index=len(request.placeholders),
            total_placeholders=len(request.placeholders),
            is_complete=True
        )
    
    # Get current placeholder
    current_placeholder = unfilled_placeholders[0]
    actual_index = request.placeholders.index(current_placeholder)
    
    try:
        # Generate question using AI
        question = await generate_chat_question(
            placeholder=current_placeholder,
            context={"filled_data": request.current_data}
        )
        
        return ChatResponse(
            question=question,
            current_placeholder=current_placeholder,
            placeholder_index=actual_index,
            total_placeholders=len(request.placeholders),
            is_complete=False
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating question: {str(e)}")

class AnswerRequest(BaseModel):
    placeholder: str
    answer: str
    current_data: Dict[str, str]

class AnswerResponse(BaseModel):
    success: bool
    updated_data: Dict[str, str]
    message: str

@router.post("/chat/answer", response_model=AnswerResponse)
async def submit_answer(request: AnswerRequest):
    """
    Submit an answer for a placeholder.
    """
    if not request.answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty")
    
    # Update the data
    updated_data = request.current_data.copy()
    updated_data[request.placeholder] = request.answer.strip()
    
    return AnswerResponse(
        success=True,
        updated_data=updated_data,
        message=f"Successfully saved answer for {request.placeholder}"
    )

@router.get("/chat/health")
async def chat_health():
    """Health check for chat service."""
    return {"status": "healthy", "service": "chat"}
