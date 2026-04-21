from __future__ import annotations

import io
import logging

import fitz
import pytesseract
from PIL import Image
from pypdf import PdfReader

from app.services.utils import join_text_blocks, looks_like_good_text, normalize_whitespace

logger = logging.getLogger(__name__)


import os
TESSERACT_LANG = os.getenv("TESSERACT_LANG", "eng+rus+chi_sim").strip() or "eng+rus+chi_sim"


def try_extract_embedded_text(content: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(content))
        parts = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        return join_text_blocks(parts)
    except Exception:
        logger.exception("Embedded PDF text extraction failed")
        return ""


def ocr_pdf_pages(content: bytes, max_pages: int = 2) -> str:
    doc = fitz.open(stream=content, filetype="pdf")
    parts: list[str] = []

    for page_index, page in enumerate(doc):
        if page_index >= max_pages:
            break

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        png_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        text = pytesseract.image_to_string(image, lang=TESSERACT_LANG)

        if text.strip():
            parts.append(text)

    return join_text_blocks(parts)


def extract_text_from_pdf_bytes(content: bytes) -> str:
    embedded_text = try_extract_embedded_text(content)
    if looks_like_good_text(embedded_text):
        return normalize_whitespace(embedded_text)

    return ocr_pdf_pages(content, max_pages=2)
