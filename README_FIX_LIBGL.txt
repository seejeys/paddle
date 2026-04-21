Updated Render OCR backend fix with libGL.

What changed:
- Dockerfile now installs libgl1
- fixes: ImportError: libGL.so.1
- keeps previous PaddleOCR constructor fix
- same endpoints and env vars

How to use:
1. Replace your OCR backend repo contents with this archive.
2. Commit and push to GitHub.
3. Render will auto-redeploy.
4. After deploy, test /health, then JPG.
