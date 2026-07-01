"""Convenience launcher for the dev server.

Resolves the project root from this file's own location, so it starts the
API reliably no matter which directory it is invoked from, or which
computer/user account the repo is checked out under. Run with:

    python run.py
"""

from pathlib import Path

import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8000

if __name__ == "__main__":
    base_url = f"http://{HOST}:{PORT}"
    print(f"Upload UI:    {base_url}/ui", flush=True)
    print(f"Swagger docs: {base_url}/docs", flush=True)
    print(f"Health check: {base_url}/health", flush=True)
    print(flush=True)

    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        app_dir=str(PROJECT_ROOT),
    )
