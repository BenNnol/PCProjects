"""PCProjects service — a small FastAPI app.

Routes: the status page at "/" and the JSON payload it renders at "/api/info".
Started by docker-compose.base44.yml with `uvicorn --reload`, so edits to this
package appear in the preview without a rebuild.

Nothing here calls an external service, so the app needs no credentials to run.
"""

import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

APP_NAME = "PCProjects"
APP_VERSION = "0.1.0"

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title=f"{APP_NAME} API", version=APP_VERSION)


@app.get("/api/info")
def info() -> dict[str, str]:
    """Status payload for the page, and the probe the compose healthcheck uses."""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "environment": os.getenv("APP_ENV", "development"),
        "server_time_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    """Serve the status page.

    Read from disk on each request, so editing the HTML only needs a refresh.
    """
    return FileResponse(STATIC_DIR / "index.html")
