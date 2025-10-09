"""
Google Gemini client utilities for placeholder extraction and conversational flow.
"""

import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json

def get_gemini_client():
    """Get Gemini client with lazy initialization."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set your GEMINI_API_KEY in the .env file")
    
    genai.configure(api_key=api_key)
    # Using 2.5-flash (latest, most cost-effective model)
    return genai.GenerativeModel('gemini-2.5-flash')

async def extract_placeholders_with_ai(document_text: str) -> List[str]:
    """
    Use Gemini to extract placeholders from document text as fallback.
    """
    system_prompt = """
    You are an AI legal assistant.
    Given a legal document, extract all placeholders like [Company Name], [Investor Name], blanks (________), or similar patterns that need to be filled.
    Return them as a JSON list of clean, descriptive strings without brackets or underscores.
    Focus on meaningful placeholders that a user would need to fill out.
    
    Example response: ["Company Name", "Investor Name", "Investment Amount", "Date"]
    """
    
    user_prompt = f"Extract placeholders from this legal document:\n\n{document_text[:3000]}"
    
    try:
        model = get_gemini_client()
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        
        content = response.text
        # Try to parse as JSON, fallback to simple list
        try:
            placeholders = json.loads(content)
            return placeholders if isinstance(placeholders, list) else []
        except:
            # Fallback: extract from text response
            lines = content.strip().split('\n')
            return [line.strip('- "[]') for line in lines if line.strip()]
            
    except Exception as e:
        print(f"Gemini API error: {e}")
        return []

async def analyze_document(document_text: str) -> str:
    """
    Analyze the document and provide a brief explanation of what it entails.
    """
    system_prompt = """
    You are an AI legal assistant. Analyze the provided legal document and give a brief, clear explanation of:
    1. What type of document this is
    2. The main purpose and key provisions
    3. Who the parties involved are (in general terms)
    4. Any important legal implications or considerations
    
    Keep your response conversational, professional, and under 200 words. Make it accessible to non-lawyers.
    IMPORTANT: Use plain text only - no markdown formatting, no asterisks, no bold text.
    """
    
    user_prompt = f"Please analyze this legal document and explain what it entails:\n\n{document_text[:4000]}"
    
    try:
        model = get_gemini_client()
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        
        # Clean up any markdown formatting that might slip through
        text = response.text.strip()
        # Remove markdown bold syntax
        text = text.replace('**', '')
        # Remove markdown italic syntax
        text = text.replace('*', '')
        # Remove extra newlines
        text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
        
        return text
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback analysis
        return "This appears to be a legal document that requires filling in specific information. I'll help you complete the placeholders step by step."

async def generate_chat_question(placeholder: str, context: Dict[str, Any] = None) -> str:
    """
    Generate a conversational question for a specific placeholder.
    """
    system_prompt = """
    You are Lexsy, a friendly and professional AI legal assistant helping someone fill out a legal document.
    
    Your personality:
    - Warm, conversational, and approachable (like a helpful colleague)
    - Use natural language, not robotic form-speak
    - Add brief helpful context or examples when relevant
    - Be encouraging and supportive
    - Keep it professional but friendly
    
    Task: Generate ONE conversational question to ask about the given field.
    - Make it feel like natural conversation (1-2 sentences max)
    - Don't just say "What is the X?" - be more creative and contextual
    - Use plain English, avoid legal jargon
    - You can acknowledge previous answers to create flow
    
    IMPORTANT: Respond with ONLY the question, no markdown, no extra formatting.
    """
    
    user_prompt = f"Ask the user about: {placeholder}"
    if context and context.get('filled_data'):
        filled = context['filled_data']
        if filled:
            recent_fields = list(filled.keys())[:2]
            user_prompt += f"\n\nPreviously filled: {', '.join(recent_fields)}"
    
    try:
        model = get_gemini_client()
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        
        # Clean up response
        text = response.text.strip()
        text = text.replace('**', '').replace('*', '').replace('_', '')
        # Remove any quotes if AI wrapped the question
        text = text.strip('"\'')
        
        return text
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback question with some personality
        return f"Great! Now, could you tell me the {placeholder.lower()}?"

async def generate_conversational_response(
    user_message: str,
    placeholders: List[str],
    current_data: Dict[str, str],
    unfilled_placeholders: List[str],
    document_text: Optional[str] = None,
    conversation_history: List[Dict[str, str]] = None,
    progress: tuple = (0, 0)
) -> Dict[str, Any]:
    """
    Generate a conversational response that can:
    - Answer questions about the document
    - Provide clarifications
    - Guide users through filling fields
    - Handle arbitrary user messages
    """
    filled_count, total_count = progress
    
    # Build conversation context
    history_text = ""
    if conversation_history:
        recent_history = conversation_history[-6:]  # Last 3 exchanges
        history_text = "\n".join([
            f"{'User' if msg.get('type') == 'user' else 'Lexsy'}: {msg.get('content', '')}"
            for msg in recent_history
        ])
    
    system_prompt = f"""
    You are Lexsy, a friendly and highly knowledgeable AI legal assistant helping someone complete a legal document through conversation.
    
    DOCUMENT CONTEXT:
    Document excerpt: {document_text[:800] if document_text else 'Legal document'}
    
    CURRENT STATUS:
    - Total fields: {total_count}
    - Completed: {filled_count} ({', '.join(list(current_data.keys())[:5]) if current_data else 'None yet'})
    - Remaining: {', '.join(unfilled_placeholders[:5]) if unfilled_placeholders else 'All done!'}
    
    YOUR PERSONALITY & APPROACH:
    - You're like a knowledgeable legal advisor friend - warm, patient, and expert
    - Engage in genuine conversation - don't just fill forms robotically
    - When users ask questions, give thoughtful, educational answers
    - Explain legal concepts in simple, everyday language
    - Share relevant context and examples when helpful
    - Be encouraging and make the user feel supported
    
    CRITICAL: DISTINGUISH BETWEEN QUESTIONS AND ANSWERS:
    - If the user asks a question (contains ?, asks about concepts, seeks clarification) → Answer their question thoroughly
    - If the user provides information (short factual statement, looks like data) → Acknowledge it and ask about the next field
    - When in doubt, treat it as a question and engage conversationally
    
    CONVERSATION STYLE:
    - Natural, flowing dialogue (2-5 sentences)
    - Plain text only - no markdown, asterisks, or formatting
    - Show personality - be human, not robotic
    - Don't be pushy about filling fields
    - Prioritize helpfulness over form completion
    
    GUIDING PRINCIPLES:
    - Answer questions FIRST before pushing to fill fields
    - Only suggest filling fields when the user seems ready
    - Make the experience educational and empowering
    - Create trust through knowledge sharing
    """
    
    user_prompt = f"""
    Conversation history:
    {history_text if history_text else 'Just starting our conversation.'}
    
    User's latest message: "{user_message}"
    
    INSTRUCTIONS:
    1. READ CAREFULLY - Is this a question or information?
    2. If it's a QUESTION (asking about concepts, seeking clarification, contains '?'):
       - Give a thoughtful, educational answer
       - Explain the concept clearly
       - Don't immediately push to fill fields
    3. If it's INFORMATION (providing data like a name, number, date):
       - Acknowledge what they provided
       - Ask about the next field naturally
    
    Respond conversationally and naturally. Be helpful, knowledgeable, and friendly.
    """
    
    try:
        model = get_gemini_client()
        # Use synchronous generate_content for better stability
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        
        # Clean up response
        text = response.text.strip()
        text = text.replace('**', '').replace('*', '').replace('_', '')
        text = text.strip('"\'')
        
        # Let the AI handle everything - don't auto-detect field filling
        # The AI's response will naturally guide the conversation
        return {
            "response": text,
            "suggested_field": None,
            "should_fill_field": False  # Let frontend handle field detection manually
        }
        
    except Exception as e:
        print(f"Gemini conversational chat error: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback response
        if unfilled_placeholders:
            return {
                "response": f"I'd be happy to help! We still need to fill in: {', '.join(unfilled_placeholders[:3])}. What would you like to know?",
                "suggested_field": None,
                "should_fill_field": False
            }
        else:
            return {
                "response": "Great! All fields are complete. What else would you like to know?",
                "suggested_field": None,
                "should_fill_field": False
            }

