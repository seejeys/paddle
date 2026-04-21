# Closeframe OCR Backend for Render (PaddleOCR)

This service is designed to run outside Supabase as a separate Docker web service on Render.
Supabase Edge Function `parse` should stay the coordinator and call this service for PDF/image OCR.

## Why this architecture

- Supabase Storage keeps uploaded source files.
- Supabase Edge Function downloads the file and forwards it to this OCR backend.
- This backend performs OCR and returns plain text.
- The Edge Function then runs your field parser and returns structured JSON to the app.

## Language strategy

This package does **not** rely on a single `lang` setting for EN/RU/ZH. Instead it loads three OCR engines:

- `lang="en"`
- `lang="ru"`
- `lang="ch"`

For each image or PDF page, it runs all three and keeps the best text result by a simple quality score.
This is a practical MVP for mixed English/Russian/Chinese documents.

## Endpoints

- `GET /health`
- `POST /ocr/pdf`
- `POST /ocr/image`

Both OCR endpoints require the `x-ocr-secret` header.

## Deploy on Render

1. Create a new GitHub repository and upload this folder.
2. In Render, click **New** -> **Web Service**.
3. Connect the repo.
4. Set **Environment** to **Docker**.
5. Add env var:
   - `OCR_SHARED_SECRET=<your long random secret>`
6. Deploy.
7. After deployment, test:
   - `GET https://<your-service>.onrender.com/health`

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OCR_SHARED_SECRET=test-secret
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Test the OCR API locally

```bash
curl -X POST http://127.0.0.1:8000/ocr/pdf \
  -H 'x-ocr-secret: test-secret' \
  -F 'file=@sample.pdf'
```

```bash
curl -X POST http://127.0.0.1:8000/ocr/image \
  -H 'x-ocr-secret: test-secret' \
  -F 'file=@sample.png'
```
