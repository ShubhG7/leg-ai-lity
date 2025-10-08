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
        
        # Replace placeholders in paragraphs
        for paragraph in doc.paragraphs:
            for placeholder, value in placeholder_data.items():
                # Replace [Placeholder] format
                bracket_pattern = f"\\[{re.escape(placeholder)}\\]"
                paragraph_text = re.sub(bracket_pattern, value, paragraph.text, flags=re.IGNORECASE)
                
                # Replace underscore format (find and replace context-based)
                # This is more complex as we need to maintain formatting
                if paragraph_text != paragraph.text:
                    # Clear existing runs and add new text
                    paragraph.clear()
                    paragraph.add_run(paragraph_text)
        
        # Replace placeholders in tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for placeholder, value in placeholder_data.items():
                            bracket_pattern = f"\\[{re.escape(placeholder)}\\]"
                            paragraph_text = re.sub(bracket_pattern, value, paragraph.text, flags=re.IGNORECASE)
                            
                            if paragraph_text != paragraph.text:
                                paragraph.clear()
                                paragraph.add_run(paragraph_text)
        
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
