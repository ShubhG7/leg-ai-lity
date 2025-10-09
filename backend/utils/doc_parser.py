"""
Document parsing utilities for extracting placeholders from .docx files.
"""

import re
from docx import Document
from typing import List, Set
from .gemini_client import extract_placeholders_with_ai

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract all text content from a .docx file.
    """
    try:
        doc = Document(file_path)
        full_text = []
        
        # Extract text from paragraphs
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text)
        
        # Extract text from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        full_text.append(cell.text)
        
        return '\n'.join(full_text)
        
    except Exception as e:
        raise Exception(f"Error reading document: {str(e)}")

def extract_placeholders_regex(text: str) -> Set[str]:
    """
    Extract placeholders using regex patterns.
    Looks for [Text], _______, and similar patterns.
    """
    placeholders = set()
    
    # Pattern 1: [Text] format
    bracket_pattern = r'\[([^\]]+)\]'
    bracket_matches = re.findall(bracket_pattern, text)
    placeholders.update(bracket_matches)
    
    # Pattern 2: Multiple underscores (3 or more)
    underscore_pattern = r'_{3,}'
    underscore_matches = re.findall(underscore_pattern, text)
    # Convert underscores to descriptive names based on context
    for match in underscore_matches:
        # Try to find context around the underscores
        context_pattern = rf'(\w+\s+)?{re.escape(match)}(\s+\w+)?'
        context_match = re.search(context_pattern, text)
        if context_match:
            before = context_match.group(1) or ""
            after = context_match.group(2) or ""
            placeholder_name = f"{before.strip()} {after.strip()}".strip() or "Field"
            placeholders.add(placeholder_name)
        else:
            placeholders.add("Field")
    
    # Pattern 3: Common legal document patterns
    legal_patterns = [
        r'(?i)(company\s+name)',
        r'(?i)(investor\s+name)',
        r'(?i)(purchase\s+amount)',
        r'(?i)(date\s+of\s+\w+)',
        r'(?i)(signature\s+date)',
        r'(?i)(effective\s+date)',
    ]
    
    for pattern in legal_patterns:
        matches = re.findall(pattern, text)
        placeholders.update([match.title() for match in matches])
    
    return placeholders

async def extract_all_placeholders(file_path: str) -> List[str]:
    """
    Extract placeholders using both regex and AI fallback.
    """
    # Extract text from document
    document_text = extract_text_from_docx(file_path)
    
    # Use regex first
    regex_placeholders = extract_placeholders_regex(document_text)
    
    # Use AI as fallback/enhancement
    ai_placeholders = await extract_placeholders_with_ai(document_text)
    
    # Combine and deduplicate
    all_placeholders = list(regex_placeholders)
    
    # Add AI-found placeholders that aren't already found
    for ai_placeholder in ai_placeholders:
        if not any(ai_placeholder.lower() in existing.lower() or existing.lower() in ai_placeholder.lower() 
                  for existing in all_placeholders):
            all_placeholders.append(ai_placeholder)
    
    # Clean up and return
    cleaned_placeholders = []
    for placeholder in all_placeholders:
        cleaned = placeholder.strip('[]_').strip()
        if cleaned and len(cleaned) > 1:
            cleaned_placeholders.append(cleaned)
    
    return list(set(cleaned_placeholders))  # Remove duplicates
