"""
Chat endpoint with full AI integration.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from utils.openai_client import generate_chat_question
from utils.auth import get_current_user, User

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

class AnswerRequest(BaseModel):
    placeholder: str
    answer: str
    current_data: Dict[str, str]

class AnswerResponse(BaseModel):
    success: bool
    updated_data: Dict[str, str]
    message: str

@router.post("/chat/question-ai", response_model=ChatResponse)
async def get_next_question_with_ai(request: ChatRequest):
    """
    Get the next question for filling placeholders with AI (no auth for demo).
    """
    if not request.placeholders:
        raise HTTPException(status_code=400, detail="No placeholders provided")
    
    # Find unfilled placeholders
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
    except Exception as e:
        print(f"AI question generation failed: {e}")
        # Fallback to simple question
        question = f"Please provide the {current_placeholder.lower()}:"
    
    return ChatResponse(
        question=question,
        current_placeholder=current_placeholder,
        placeholder_index=actual_index,
        total_placeholders=len(request.placeholders),
        is_complete=False
    )

@router.post("/chat/answer-ai", response_model=AnswerResponse)
async def submit_answer_with_ai(request: AnswerRequest):
    """
    Submit an answer for a placeholder with AI (no auth for demo).
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
