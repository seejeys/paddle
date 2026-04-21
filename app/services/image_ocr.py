from __future__ import annotations

import logging
import os

import numpy as np
from paddleocr import PaddleOCR

from app.services.utils import join_text_blocks, pil_image_from_bytes

logger = logging.getLogger(__name__)

PADDLE_LANG = os.getenv("PADDLE_LANG", "en").strip() or "en"

_ocr = None


def get_ocr() -> PaddleOCR:
    global _ocr
    if _ocr is None:
        logger.info("Initializing PaddleOCR with lang=%s", PADDLE_LANG)
        _ocr = PaddleOCR(lang=PADDLE_LANG)
    return _ocr


def extract_text_from_image_bytes(content: bytes) -> str:
    image = pil_image_from_bytes(content)
    arr = np.array(image)

    try:
        ocr = get_ocr()
        result = ocr.predict(arr)
    except Exception:
        logger.exception("PaddleOCR image predict failed")
        raise

    blocks: list[str] = []

    for item in result:
        rec_texts = item.get("rec_texts", [])
        if rec_texts:
            blocks.extend(str(x) for x in rec_texts if x)

    return join_text_blocks(blocks)
