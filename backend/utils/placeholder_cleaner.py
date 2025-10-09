"""
Advanced placeholder cleaning and standardization for legal documents.
"""

import re
from typing import List, Set

def clean_and_standardize_placeholders(placeholders: Set[str]) -> List[str]:
    """
    Clean and standardize placeholders to ensure they're perfect for legal documents.
    """
    # Define standard legal field mappings
    STANDARD_FIELD_MAPPINGS = {
        'investor name': 'Investor Name',
        'company name': 'Company Name', 
        'purchase amount': 'Purchase Amount',
        'date of safe': 'Date of Safe',
        'effective date': 'Effective Date',
        'state of incorporation': 'State of Incorporation',
        'governing law jurisdiction': 'Governing Law Jurisdiction',
        'governing law': 'Governing Law',
        'notice address': 'Notice Address',
        'email address': 'Email Address',
        'phone number': 'Phone Number',
        'signature date': 'Signature Date',
        'closing date': 'Closing Date',
        'valuation cap': 'Valuation Cap',
        'discount rate': 'Discount Rate',
        'pro rata rights': 'Pro Rata Rights',
    }
    
    # Clean up placeholders
    cleaned = set()
    
    for placeholder in placeholders:
        # Normalize the placeholder
        normalized = re.sub(r'\s+', ' ', placeholder.strip().lower())
        
        # Skip if too short or too long
        if len(normalized) < 3 or len(normalized) > 50:
            continue
            
        # Skip generic terms
        if normalized in ['title', 'field', 'name', 'company', 'blank', 'date']:
            continue
            
        # Check if it matches a standard field
        if normalized in STANDARD_FIELD_MAPPINGS:
            cleaned.add(STANDARD_FIELD_MAPPINGS[normalized])
        else:
            # Capitalize properly
            cleaned.add(normalized.title())
    
    # Remove duplicates and merge similar ones
    final_placeholders = []
    placeholder_list = list(cleaned)
    
    for placeholder in placeholder_list:
        # Check for duplicates
        is_duplicate = False
        for existing in final_placeholders:
            # Normalize both for comparison
            norm_placeholder = re.sub(r'\s+', ' ', placeholder.lower().strip())
            norm_existing = re.sub(r'\s+', ' ', existing.lower().strip())
            
            if norm_placeholder == norm_existing:
                is_duplicate = True
                break
                
        if not is_duplicate:
            final_placeholders.append(placeholder)
    
    # Sort for consistency
    final_placeholders.sort()
    
    return final_placeholders
