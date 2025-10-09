"""
Document filling utilities for replacing placeholders with user data.
"""

import re
from docx import Document
from typing import Dict
import os

def fill_document_placeholders(input_file_path: str, output_file_path: str, placeholder_data: Dict[str, str]) -> str:
    """
    Fill placeholders in a .docx document with provided data.
    Returns the path to the filled document.
    """
    try:
        # Load the document
        doc = Document(input_file_path)
        
        # Create a mapping of original placeholders to cleaned values
        # This handles case-insensitive matching and formatting
        placeholder_mapping = {}
        for key, value in placeholder_data.items():
            # Create variations of the placeholder for matching
            variations = [
                key,  # Original
                key.title(),  # Title case
                key.lower(),  # Lower case
                key.upper(),  # Upper case
                f"[{key}]",  # With brackets
                f"[{key.title()}]",  # With brackets, title case
                f"[{key.lower()}]",  # With brackets, lower case
                f"[{key.upper()}]",  # With brackets, upper case
            ]
            for variation in variations:
                placeholder_mapping[variation] = value
        
        # Replace placeholders in paragraphs
        for paragraph in doc.paragraphs:
            original_text = paragraph.text
            new_text = original_text
            
            # Replace bracket placeholders first (most precise)
            for placeholder, value in placeholder_data.items():
                # Try different bracket formats
                patterns = [
                    f"\\[{re.escape(placeholder)}\\]",
                    f"\\[{re.escape(placeholder.title())}\\]",
                    f"\\[{re.escape(placeholder.lower())}\\]",
                    f"\\[{re.escape(placeholder.upper())}\\]",
                ]
                
                for pattern in patterns:
                    new_text = re.sub(pattern, value, new_text, flags=re.IGNORECASE)
            
            # Replace dollar amount placeholders like $[Amount]
            for placeholder, value in placeholder_data.items():
                if any(keyword in placeholder.lower() for keyword in ['amount', 'price', 'value', 'cost', 'investment', 'purchase']):
                    dollar_patterns = [
                        f"\\$\\[{re.escape(placeholder)}\\]",
                        f"\\$\\[{re.escape(placeholder.title())}\\]",
                    ]
                    for pattern in dollar_patterns:
                        # Format monetary values properly
                        if value.replace('.', '').replace(',', '').isdigit():
                            formatted_value = f"${value}" if not value.startswith('$') else value
                        else:
                            formatted_value = value
                        new_text = re.sub(pattern, formatted_value, new_text, flags=re.IGNORECASE)
            
            # Update paragraph if text changed
            if new_text != original_text:
                paragraph.clear()
                paragraph.add_run(new_text)
        
        # Replace placeholders in tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        original_text = paragraph.text
                        new_text = original_text
                        
                        # Apply same replacement logic as paragraphs
                        for placeholder, value in placeholder_data.items():
                            patterns = [
                                f"\\[{re.escape(placeholder)}\\]",
                                f"\\[{re.escape(placeholder.title())}\\]",
                                f"\\[{re.escape(placeholder.lower())}\\]",
                                f"\\[{re.escape(placeholder.upper())}\\]",
                            ]
                            
                            for pattern in patterns:
                                new_text = re.sub(pattern, value, new_text, flags=re.IGNORECASE)
                        
                        if new_text != original_text:
                            paragraph.clear()
                            paragraph.add_run(new_text)
        
        # Handle underscore placeholders with more sophisticated matching
        _replace_underscore_placeholders(doc, placeholder_data)
        
        # Save the filled document
        doc.save(output_file_path)
        return output_file_path
        
    except Exception as e:
        raise Exception(f"Error filling document: {str(e)}")

def _replace_underscore_placeholders(doc: Document, placeholder_data: Dict[str, str]):
    """
    Replace underscore placeholders (___) with appropriate values based on context.
    """
    # This is a simplified approach - in production, you'd want more sophisticated matching
    underscore_pattern = r'_{3,}'
    
    # Create a list of values to use for underscore replacements
    values_list = list(placeholder_data.values())
    value_index = 0
    
    for paragraph in doc.paragraphs:
        if re.search(underscore_pattern, paragraph.text):
            new_text = paragraph.text
            
            # Replace underscores with values in order
            while re.search(underscore_pattern, new_text) and value_index < len(values_list):
                new_text = re.sub(underscore_pattern, values_list[value_index], new_text, count=1)
                value_index += 1
            
            if new_text != paragraph.text:
                paragraph.clear()
                paragraph.add_run(new_text)
    
    # Do the same for tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if re.search(underscore_pattern, paragraph.text):
                        new_text = paragraph.text
                        
                        while re.search(underscore_pattern, new_text) and value_index < len(values_list):
                            new_text = re.sub(underscore_pattern, values_list[value_index], new_text, count=1)
                            value_index += 1
                        
                        if new_text != paragraph.text:
                            paragraph.clear()
                            paragraph.add_run(new_text)
