"""
Field utilities: normalization/validation endpoints for interactive UI.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from utils.doc_filler import normalize_placeholder_values

try:
    from utils.gemini_client import get_gemini_client
except Exception:  # pragma: no cover
    get_gemini_client = None  # type: ignore


router = APIRouter()


class NormalizeRequest(BaseModel):
    field: str
    value: str
    use_ai: Optional[bool] = True


class NormalizeResponse(BaseModel):
    normalized: str


@router.post("/fields/normalize", response_model=NormalizeResponse)
async def normalize_field(req: NormalizeRequest):
    """Normalize a single field value using rules, optionally refined by AI.

    - Money → $X,XXX,XXX(.XX)
    - Dates → Month DD, YYYY
    - Names/titles → Title Case
    - Emails → lowercase
    """
    # Rule-based normalization first (fast, deterministic)
    rule_norm = normalize_placeholder_values({req.field: req.value}).get(req.field, req.value)

    # Optional AI refinement
    if req.use_ai and os.getenv("GEMINI_API_KEY") and get_gemini_client:
        try:
            model = get_gemini_client()
            system = (
                "You normalize a single field for a legal document. Return ONLY the normalized value. "
                "Rules: Dates => 'Month DD, YYYY'; Money => '$' + thousands separators; "
                "Emails lowercase; Names/Companies Title Case; Keep addresses as provided but tidy spaces."
            )
            prompt = (
                f"Field: {req.field}\n"
                f"Original: {req.value}\n"
                f"RuleNormalized: {rule_norm}\n"
                "Return the best normalized value only, no extra text."
            )
            resp = model.generate_content(f"{system}\n\n{prompt}")
            text = (resp.text or "").strip().strip('"')
            if text:
                rule_norm = text
        except Exception:
            # Fall back silently to rule_norm
            pass

    return NormalizeResponse(normalized=rule_norm)


