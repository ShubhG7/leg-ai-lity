"""
OpenAI client utilities for placeholder extraction and conversational flow.
"""

import os
from openai import OpenAI
from typing import List, Dict, Any
import json

def get_openai_client():
    """Get OpenAI client with lazy initialization."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        raise ValueError("Please set your OPENAI_API_KEY in the .env file")
    return OpenAI(api_key=api_key)

async def extract_placeholders_with_ai(document_text: str) -> List[str]:
    """
    Use GPT-4o-mini to extract placeholders from document text as fallback.
    """
    system_prompt = """
    You are an AI legal assistant.
    Given a legal document, extract all placeholders like [Company Name], [Investor Name], blanks (________), or similar patterns that need to be filled.
    Return them as a JSON list of clean, descriptive strings without brackets or underscores.
    Focus on meaningful placeholders that a user would need to fill out.
    """
    
    user_prompt = f"Extract placeholders from this legal document:\n\n{document_text[:3000]}"
    
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        # Try to parse as JSON, fallback to simple list
        try:
            placeholders = json.loads(content)
            return placeholders if isinstance(placeholders, list) else []
        except:
            # Fallback: extract from text response
            lines = content.strip().split('\n')
            return [line.strip('- "[]') for line in lines if line.strip()]
            
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return []

async def generate_chat_question(placeholder: str, context: Dict[str, Any] = None) -> str:
    """
    Generate a conversational question for a specific placeholder.
    """
    system_prompt = """
    You are an AI that helps fill legal forms conversationally.
    Generate one clear, professional question to ask the user for the given placeholder.
    Keep it concise and user-friendly. Don't use legal jargon unnecessarily.
    """
    
    user_prompt = f"Generate a question to ask the user for this placeholder: {placeholder}"
    if context:
        user_prompt += f"\nContext: {context}"
    
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Fallback question
        return f"Please provide the {placeholder.lower()}:"
