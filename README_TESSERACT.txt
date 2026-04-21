Closeframe Render OCR backend (Tesseract)

What this is:
- Drop-in replacement for the Render Paddle backend
- Same endpoints:
  - GET /health
  - POST /ocr/pdf
  - POST /ocr/image
- Compatible with the current Supabase parse function hook

Why use this:
- Much lighter startup on free Render
- No large Paddle model downloads on container boot
- More stable MVP for JPG/PDF OCR

How to deploy:
1. Replace your OCR backend repo contents with this archive.
2. Commit and push to GitHub.
3. Render auto-redeploys.
4. Keep env vars:
   - OCR_SHARED_SECRET = same secret as Supabase OCR_SHARED_SECRET
   - TESSERACT_LANG = eng+rus+chi_sim

Notes:
- PDF flow tries embedded text first.
- If embedded text is weak, it OCRs first 2 pages.
- You do NOT need to change Supabase parse/index.ts for this backend.
