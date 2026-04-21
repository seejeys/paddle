from __future__ import annotations

import numpy as np

from app.services.ocr_router import run_best_of_three_ocr
from app.services.utils import pil_image_from_bytes


def extract_text_from_image_bytes(content: bytes) -> str:
    image = pil_image_from_bytes(content)
    arr = np.array(image)
    _lang, text = run_best_of_three_ocr(arr)
    return text.strip()
