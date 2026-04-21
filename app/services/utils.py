from __future__ import annotations

import io
import re
from typing import Iterable

from PIL import Image


def normalize_whitespace(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def pil_image_from_bytes(content: bytes) -> Image.Image:
    return Image.open(io.BytesIO(content)).convert("RGB")


def join_text_blocks(blocks: Iterable[str]) -> str:
    return normalize_whitespace("\n\n".join(x.strip() for x in blocks if x and x.strip()))


def looks_like_good_text(text: str) -> bool:
    cleaned = normalize_whitespace(text)
    if len(cleaned) < 40:
        return False
    alpha_num = re.findall(r"[A-Za-zА-Яа-я0-9\u4E00-\u9FFF]", cleaned)
    return len(alpha_num) >= 20
