"""
Chat endpoint with Gemini AI integration.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from utils.gemini_client import generate_chat_question

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

@router.post("/chat/question-gemini", response_model=ChatResponse)
async def get_next_question_with_gemini(request: ChatRequest):
    """
    Get the next question for filling placeholders with Gemini AI.
    """
    if not request.placeholders:
        raise HTTPException(status_code=400, detail="No placeholders provided")
    
    # Find unfilled placeholders
    unfilled_placeholders = [p for p in request.placeholders if p not in request.current_data]
    
    if not unfilled_placeholders:
        return ChatResponse(
            question="Perfect! All placeholders have been filled. You can now generate your completed document.",
            current_placeholder="",
            placeholder_index=len(request.placeholders),
            total_placeholders=len(request.placeholders),
            is_complete=True
        )
    
    # Get current placeholder
    current_placeholder = unfilled_placeholders[0]
    actual_index = request.placeholders.index(current_placeholder)
    
    # COST-OPTIMIZED: Use Gemini for complex placeholders, conversational simple questions for obvious ones
    simple_placeholders_map = {
        'name': "What's the name",
        'date': "What date",
        'amount': "How much",
        'email': "What's the email address",
        'phone': "What's the phone number",
        'address': "What's the address",
    }
    
    # Check if it's a simple placeholder
    is_simple = False
    simple_question_start = None
    for keyword, question_start in simple_placeholders_map.items():
        if keyword in current_placeholder.lower():
            is_simple = True
            simple_question_start = question_start
            break
    
    if is_simple and simple_question_start:
        # Use conversational simple question for obvious placeholders (cost optimization)
        # Add variety with greetings based on progress
        progress = len(request.current_data)
        if progress == 0:
            greeting = "Let's start! "
        elif progress < 3:
            greeting = "Great! "
        else:
            greeting = "Perfect! "
        
        question = f"{greeting}{simple_question_start} for this document?"
        print(f"Using conversational simple question for: {current_placeholder}")
    else:
        try:
            # Use Gemini AI for complex/legal-specific placeholders
            print(f"Using Gemini AI for complex placeholder: {current_placeholder}")
            question = await generate_chat_question(
                placeholder=current_placeholder,
                context={"filled_data": request.current_data}
            )
        except Exception as e:
            print(f"Gemini question generation failed: {e}")
            # Fallback to conversational question
            progress = len(request.current_data)
            greeting = "Great!" if progress > 0 else "Let's start!"
            question = f"{greeting} Could you tell me the {current_placeholder.lower()}?"
    
    return ChatResponse(
        question=question,
        current_placeholder=current_placeholder,
        placeholder_index=actual_index,
        total_placeholders=len(request.placeholders),
        is_complete=False
    )

@router.post("/chat/answer-gemini", response_model=AnswerResponse)
async def submit_answer_with_gemini(request: AnswerRequest):
    """
    Submit an answer for a placeholder with Gemini AI.
    """
    if not request.answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty")
    
    # Update the data
    updated_data = request.current_data.copy()
    updated_data[request.placeholder] = request.answer.strip()
    
    return AnswerResponse(
        success=True,
        updated_data=updated_data,
        message=f"Great! I've saved '{request.answer.strip()}' for {request.placeholder}."
    )
