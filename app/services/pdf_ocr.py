from __future__ import annotations

import io

import fitz
import numpy as np
from PIL import Image

from app.services.ocr_router import run_best_of_three_ocr
from app.services.utils import join_text_blocks, looks_like_good_text


def try_extract_embedded_text(content: bytes) -> str:
    doc = fitz.open(stream=content, filetype="pdf")
    parts: list[str] = []

    for page in doc:
        text = page.get_text("text") or ""
        if text.strip():
            parts.append(text)

    return join_text_blocks(parts)


def ocr_pdf_pages(content: bytes) -> str:
    doc = fitz.open(stream=content, filetype="pdf")
    parts: list[str] = []

    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        png_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        arr = np.array(image)
        _lang, text = run_best_of_three_ocr(arr)
        if text.strip():
            parts.append(text.strip())

    return join_text_blocks(parts)


def extract_text_from_pdf_bytes(content: bytes) -> str:
    embedded_text = try_extract_embedded_text(content)
    if looks_like_good_text(embedded_text):
        return embedded_text

    return ocr_pdf_pages(content)
