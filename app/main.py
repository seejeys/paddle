import logging
import os

from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.services.pdf_ocr import extract_text_from_pdf_bytes
from app.services.image_ocr import extract_text_from_image_bytes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Closeframe OCR Backend (Tesseract)")

OCR_SHARED_SECRET = os.getenv("OCR_SHARED_SECRET", "").strip()


def verify_secret(x_ocr_secret: str | None) -> None:
    if not OCR_SHARED_SECRET:
        raise HTTPException(status_code=500, detail="OCR_SHARED_SECRET is not set")
    if not x_ocr_secret or x_ocr_secret != OCR_SHARED_SECRET:
        raise HTTPException(status_code=401, detail="Invalid OCR secret")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/ocr/pdf")
async def ocr_pdf(
    file: UploadFile = File(...),
    x_ocr_secret: str | None = Header(default=None),
):
    verify_secret(x_ocr_secret)

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        text = extract_text_from_pdf_bytes(content)
        return JSONResponse({"text": text})
    except Exception as e:
        logger.exception("PDF OCR failed")
        raise HTTPException(status_code=500, detail=f"PDF OCR failed: {e}")


@app.post("/ocr/image")
async def ocr_image(
    file: UploadFile = File(...),
    x_ocr_secret: str | None = Header(default=None),
):
    verify_secret(x_ocr_secret)

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        text = extract_text_from_image_bytes(content)
        return JSONResponse({"text": text})
    except Exception as e:
        logger.exception("Image OCR failed")
        raise HTTPException(status_code=500, detail=f"Image OCR failed: {e}")
