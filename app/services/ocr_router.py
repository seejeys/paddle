from __future__ import annotations

from functools import lru_cache
from typing import List, Tuple

import numpy as np
from paddleocr import PaddleOCR

from app.services.utils import join_text_blocks, score_text_quality


@lru_cache(maxsize=1)
def get_ocr_eng() -> PaddleOCR:
    return PaddleOCR(use_angle_cls=True, lang="en", show_log=False)


@lru_cache(maxsize=1)
def get_ocr_rus() -> PaddleOCR:
    return PaddleOCR(use_angle_cls=True, lang="ru", show_log=False)


@lru_cache(maxsize=1)
def get_ocr_ch() -> PaddleOCR:
    return PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)


def _collect_text(result) -> str:
    lines: List[str] = []
    if not result:
        return ""

    for page in result:
        if not page:
            continue
        for item in page:
            if len(item) >= 2 and isinstance(item[1], (list, tuple)) and item[1]:
                text = str(item[1][0]).strip()
                if text:
                    lines.append(text)
    return join_text_blocks(lines)


def run_best_of_three_ocr(image_array: np.ndarray) -> Tuple[str, str]:
    candidates = []
    for name, engine in [
        ("en", get_ocr_eng()),
        ("ru", get_ocr_rus()),
        ("ch", get_ocr_ch()),
    ]:
        result = engine.ocr(image_array, cls=True)
        text = _collect_text(result)
        candidates.append((name, text, score_text_quality(text)))

    best_name, best_text, _ = max(candidates, key=lambda x: x[2])
    return best_name, best_text
