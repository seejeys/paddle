from __future__ import annotations

import os

import pytesseract

from app.services.utils import normalize_whitespace, pil_image_from_bytes

TESSERACT_LANG = os.getenv("TESSERACT_LANG", "eng+rus+chi_sim").strip() or "eng+rus+chi_sim"


def extract_text_from_image_bytes(content: bytes) -> str:
    image = pil_image_from_bytes(content)
    text = pytesseract.image_to_string(image, lang=TESSERACT_LANG)
    return normalize_whitespace(text)
