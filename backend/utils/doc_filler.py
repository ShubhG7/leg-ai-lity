"""
Document filling utilities for replacing placeholders with user data.
"""

import re
from docx import Document
from typing import Dict
from datetime import datetime
import re as _re


def _normalize_money(raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        return s
    s_lower = s.lower().replace(" ", "")
    # 8m, 8M, 8 million, 8,000,000, $8000000
    m = _re.match(r"^\$?([0-9][0-9,]*)(\.[0-9]+)?$", s.replace(" ", ""))
    if m:
        num = float((m.group(1) + (m.group(2) or "")).replace(",", ""))
        return f"${num:,.2f}".rstrip("0").rstrip(".")
    m = _re.match(r"^\$?([0-9]+)(m|million)$", s_lower)
    if m:
        num = float(m.group(1)) * 1_000_000
        return f"${num:,.0f}"
    m = _re.match(r"^\$?([0-9]+)(k|thousand)$", s_lower)
    if m:
        num = float(m.group(1)) * 1_000
        return f"${num:,.0f}"
    # Already starts with $
    if s.startswith("$"):
        return s
    return s


def _normalize_date(raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        return s
    # Try multiple common formats without extra deps
    candidates = [
        "%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y",
        "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y",
    ]
    for fmt in candidates:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%B %d, %Y")
        except Exception:
            pass
    # Simple natural language like "Oct 9 2025" or "October 9 2025"
    try:
        # Insert comma if "Month D YYYY"
        m = _re.match(r"^(\w+)\s+(\d{1,2}),?\s+(\d{4})$", s)
        if m:
            dt = datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%B %d %Y")
            return dt.strftime("%B %d, %Y")
    except Exception:
        pass
    return s


def _normalize_email(raw: str) -> str:
    s = (raw or "").strip()
    if _re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", s):
        return s.lower()
    return s


def _title_case_name(raw: str) -> str:
    s = (raw or "").strip()
    return " ".join([w.capitalize() if w else w for w in s.split()])


def normalize_placeholder_values(data: Dict[str, str]) -> Dict[str, str]:
    """Normalize user-provided values based on placeholder names."""
    normalized: Dict[str, str] = {}
    for key, value in (data or {}).items():
        v = (value or "").strip().strip('"\'')
        kl = key.lower()
        if any(x in kl for x in ["amount", "price", "valuation", "purchase", "cap", "investment"]):
            v = _normalize_money(v)
        elif any(x in kl for x in ["date", "day", "closing", "effective"]):
            v = _normalize_date(v)
        elif "email" in kl:
            v = _normalize_email(v)
        elif any(x in kl for x in ["name", "investor", "company", "title"]):
            v = _title_case_name(v)
        normalized[key] = v
    return normalized
import os

def fill_document_placeholders(input_file_path: str, output_file_path: str, placeholder_data: Dict[str, str]) -> str:
    """
    Fill placeholders in a .docx document with provided data.
    Returns the path to the filled document.
    """
    try:
        # Load the document
        doc = Document(input_file_path)

        # Normalize incoming values up-front
        data_normalized = normalize_placeholder_values(placeholder_data)

        # Build a normalization map for placeholder keys so that
        # "Company Name", "company_name" and "COMPANY name" all map identically
        def normalize_key(s: str) -> str:
            return _re.sub(r"[^a-z0-9]", "", (s or "").lower())

        normalized_map: Dict[str, str] = {}
        for k, v in (data_normalized or {}).items():
            normalized_map[normalize_key(k)] = v
        
        # Replace placeholders in paragraphs
        for paragraph in doc.paragraphs:
            original_text = paragraph.text
            new_text = original_text
            
            # Replace [Placeholder] by normalizing the name between brackets
            def repl_brackets(m: re.Match[str]) -> str:
                inside = m.group(1)
                key = normalize_key(inside)
                return normalized_map.get(key, m.group(0))

            new_text = re.sub(r"\[([^\]]+)\]", repl_brackets, new_text)

            # Replace $[Placeholder] with normalized monetary value
            def repl_dollar(m: re.Match[str]) -> str:
                inside = m.group(1)
                key = normalize_key(inside)
                val = normalized_map.get(key)
                return _normalize_money(val) if val is not None else m.group(0)

            new_text = re.sub(r"\$\[([^\]]+)\]", repl_dollar, new_text)
            
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
                        
                        # Apply same replacement logic as paragraphs using normalized mapping
                        def repl_brackets_cell(m: re.Match[str]) -> str:
                            inside = m.group(1)
                            key = normalize_key(inside)
                            return normalized_map.get(key, m.group(0))

                        new_text = re.sub(r"\[([^\]]+)\]", repl_brackets_cell, new_text)

                        def repl_dollar_cell(m: re.Match[str]) -> str:
                            inside = m.group(1)
                            key = normalize_key(inside)
                            val = normalized_map.get(key)
                            return _normalize_money(val) if val is not None else m.group(0)

                        new_text = re.sub(r"\$\[([^\]]+)\]", repl_dollar_cell, new_text)
                        
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
    
    # Helper to find best value based on context
    def resolve_value_for_context(context_text: str) -> str | None:
        ct = (context_text or "").lower()
        best_key = None
        # Prefer keys whose words appear in context
        for k in placeholder_data.keys():
            kl = k.lower()
            if any(word in ct for word in kl.split()):
                best_key = k
                # Stronger preference for address/email/name/amount
                if any(x in kl for x in ["address", "email", "name", "amount", "date", "title"]):
                    return placeholder_data[k]
        return placeholder_data.get(best_key) if best_key else None
    
    for paragraph in doc.paragraphs:
        if re.search(underscore_pattern, paragraph.text):
            new_text = paragraph.text
            
            # Replace each run based on local context (e.g., lines containing Address:, Email:, Name:)
            while re.search(underscore_pattern, new_text):
                ctx_val = resolve_value_for_context(new_text)
                replacement = ctx_val or ""
                new_text = re.sub(underscore_pattern, replacement, new_text, count=1)
            
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
                        
                        while re.search(underscore_pattern, new_text):
                            ctx_val = resolve_value_for_context(new_text)
                            replacement = ctx_val or ""
                            new_text = re.sub(underscore_pattern, replacement, new_text, count=1)
                        
                        if new_text != paragraph.text:
                            paragraph.clear()
                            paragraph.add_run(new_text)
