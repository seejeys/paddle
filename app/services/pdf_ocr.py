from __future__ import annotations

import io
import logging

import fitz
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

from app.services.utils import join_text_blocks, looks_like_good_text
from app.services.image_ocr import get_ocr

logger = logging.getLogger(__name__)


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
    ocr: PaddleOCR = get_ocr()
    parts: list[str] = []

    for page_index, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        png_bytes = pix.tobytes("png")

        image = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        arr = np.array(image)

        try:
            result = ocr.predict(arr)
        except Exception:
            logger.exception("PaddleOCR PDF predict failed on page %s", page_index)
            raise

        for item in result:
            rec_texts = item.get("rec_texts", [])
            if rec_texts:
                parts.extend(str(x) for x in rec_texts if x)

    return join_text_blocks(parts)


def extract_text_from_pdf_bytes(content: bytes) -> str:
    embedded_text = try_extract_embedded_text(content)
    if looks_like_good_text(embedded_text):
        return embedded_text

    return ocr_pdf_pages(content)
