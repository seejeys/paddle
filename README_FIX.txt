Updated Render OCR backend fix.

What changed:
- removed unsupported PaddleOCR constructor args
- now uses: PaddleOCR(lang=PADDLE_LANG)
- added traceback logging for /ocr/pdf and /ocr/image
- keeps same endpoints and env vars

How to use:
1. Replace your OCR backend repo contents with this archive.
2. Commit and push to GitHub.
3. Render will auto-redeploy.
4. Test JPG first, then PDF.

Env vars in Render:
- OCR_SHARED_SECRET = same secret as in Supabase secret OCR_SHARED_SECRET
- PADDLE_LANG = en or ru or ch

Recommended first:
- start with PADDLE_LANG=en
- if needed create separate services later for ru/ch
