"""
Google Gemini client utilities for placeholder extraction and conversational flow.
"""

import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    Use Gemini to extract ALL placeholders from document text with high accuracy.
    """
    system_prompt = """
    You are an expert legal document analyzer specializing in comprehensive placeholder detection.
    
    TASK: Extract ALL placeholders that need to be filled in this legal document.
    
    CRITICAL REQUIREMENTS:
    1. Find EVERY single placeholder in the document - don't miss any!
    2. Look for ALL formats: [text], _____, $[text], (text), etc.
    3. Include ALL instances, even if they appear multiple times
    4. Convert to clean, descriptive field names
    5. Expect 15-20 placeholders in a typical legal document
    6. Return as a JSON array of strings
    
    PLACEHOLDER FORMATS TO DETECT:
    - [Company Name] → "Company Name"
    - [Investor Name] → "Investor Name" 
    - [Date of Safe] → "Date of Safe"
    - $[Purchase Amount] → "Purchase Amount"
    - [State of Incorporation] → "State of Incorporation"
    - [Governing Law Jurisdiction] → "Governing Law Jurisdiction"
    - [Valuation Cap] → "Valuation Cap"
    - [Discount Rate] → "Discount Rate"
    - _____ → "Signature Field" or "Address Field" (based on context)
    - [Email] → "Email Address"
    - [Phone] → "Phone Number"
    - [Address] → "Address"
    - Signature lines, dates, amounts, names, addresses, etc.
    
    EXAMPLES:
    Input: "payment by [Investor Name] of $[Purchase Amount] on [Date], [Company Name] located at [Address]"
    Output: ["Investor Name", "Purchase Amount", "Date", "Company Name", "Address"]
    
    Input: "Signatures: Investor: _____ Date: _____ Company: _____ Date: _____"
    Output: ["Investor Signature", "Investor Date", "Company Signature", "Company Date"]
    
    ULTIMATE GOAL: Find ALL placeholders. A SAFE agreement typically has 15-20 fields.
    Return ONLY a JSON array, no other text.
    """
    
    user_prompt = f"""Analyze this legal document and extract ALL placeholders that need to be filled. Return as JSON array:

{document_text}

IMPORTANT: This document likely has 15-20 placeholders. Make sure you find ALL of them including:
- All bracket placeholders [text]
- All underscore placeholders _____
- All dollar amount placeholders $[text]
- Signature lines, dates, addresses, email fields, etc.
- Pay special attention to the signature section at the end

SCAN THE ENTIRE DOCUMENT SYSTEMATICALLY:
1. Look at the beginning for company/investor info
2. Look at the middle for financial terms
3. Look at the end for signature fields
4. Count each placeholder you find

JSON array of placeholders:"""
    
    try:
        model = get_gemini_client()
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        
        # Parse the response
        response_text = response.text.strip()
        print(f"Gemini raw response: {response_text[:200]}...")
        
        # Try to extract JSON array
        try:
            # Look for JSON array in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                placeholders = json.loads(json_str)
                print(f"Gemini extracted {len(placeholders)} placeholders")
                return placeholders
        except Exception as e:
            print(f"JSON parsing error: {e}")
        
        # Fallback: extract from text
        lines = response_text.split('\n')
        placeholders = []
        for line in lines:
            line = line.strip()
            if line and ('"' in line or "'" in line):
                # Extract quoted strings
                import re
                quotes = re.findall(r'["\']([^"\']+)["\']', line)
                placeholders.extend(quotes)
        
        if not placeholders:
            # Last resort: split by common delimiters
            for delimiter in [',', ';', '\n']:
                if delimiter in response_text:
                    parts = response_text.split(delimiter)
                    for part in parts:
                        part = part.strip('"\'[] \n')
                        if part and len(part) > 2:
                            placeholders.append(part)
                    break
        
        print(f"Gemini fallback extracted {len(placeholders)} placeholders")
        return placeholders[:25]  # Limit to 25 placeholders
        
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

    STRUCTURED DATA EXTRACTION:
    - When the user provides information that maps to known placeholders, extract it as structured JSON.
    - Use the provided placeholders list to decide the canonical placeholder name.
    - Normalize values (e.g., trim quotes and leading phrases like "the", capitalize names like companies and people):
      Examples: "company name is shasha" → {"Company Name": "Shasha"}
               "valuation cap: 8m" → {"Valuation Cap": "$8,000,000"}
               "email is test@ex.com" → {"Email Address": "test@ex.com"}
    - Return both a conversational reply and a machine-readable map extracted_fields.
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
    4. Attempt structured extraction:
       - Decide if this message contains values for any of these placeholders: {placeholders}
       - Use exact placeholder names from that list where possible (case-insensitive match)
       - If a close match exists (ignoring case, punctuation, spacing), use that canonical placeholder
       - Output JSON with keys as placeholder names and values as normalized user values.
    
    Respond conversationally and naturally. Be helpful, knowledgeable, and friendly.
    
    Return your result in a 2-part format separated by a unique delimiter line:
    ===RESPONSE===
    [Your conversational response here]
    ===EXTRACTED_FIELDS_JSON===
    {{ "placeholder": "value", ... }} or {{}} if none
    """
    
    try:
        model = get_gemini_client()
        # Use synchronous generate_content for better stability
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        
        # Clean up response
        raw = response.text or ""
        raw = raw.strip()
        # Split by delimiter
        conversational = raw
        extracted_fields: Dict[str, str] = {}
        if '===EXTRACTED_FIELDS_JSON===' in raw:
            parts = raw.split('===EXTRACTED_FIELDS_JSON===')
            conversational = parts[0].replace('===RESPONSE===', '').strip()
            json_part = parts[1].strip()
            # Attempt to load JSON object from the tail
            try:
                # find JSON braces
                start = json_part.find('{')
                end = json_part.rfind('}')
                if start != -1 and end != -1 and end > start:
                    json_str = json_part[start:end+1]
                    extracted_fields = json.loads(json_str)
            except Exception as _:
                extracted_fields = {}

        conversational = conversational.replace('**', '').replace('*', '').replace('_', '').strip('"\'').strip()

        # Normalize keys to canonical placeholders based on provided list (case/punct-insensitive)
        def normalize_key(s: str) -> str:
            import re as _re
            return _re.sub(r'[^a-z0-9]', '', s.lower())

        canon_map = {normalize_key(p): p for p in placeholders}
        normalized_extracted: Dict[str, str] = {}
        for k, v in (extracted_fields or {}).items():
            nk = normalize_key(k)
            canon = canon_map.get(nk)
            if not canon:
                # try looser match by removing spaces only
                canon = next((p for n,p in canon_map.items() if n == nk), None)
            if canon and isinstance(v, str):
                val = v.strip().strip('"\'')
                # Simple capitalization for names
                if 'name' in canon.lower():
                    val = val[:1].upper() + val[1:] if val else val
                normalized_extracted[canon] = val

        return {
            "response": conversational,
            "suggested_field": None,
            "should_fill_field": bool(normalized_extracted),
            "extracted_fields": normalized_extracted or None,
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

