import os
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
SKIP_ROUTES = ("api/")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)
app.mount("/js", StaticFiles(directory=PUBLIC_DIR / "js"), name="js")
app.mount("/css", StaticFiles(directory=PUBLIC_DIR / "css"), name="css")
app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

@app.get("/manifest.json")
async def serve_manifest():
    return FileResponse(PUBLIC_DIR / "manifest.json")

@app.get("/favicon.ico")
async def serve_favicon():
    return FileResponse(PUBLIC_DIR / "favicon.ico")

@app.get("/api/hello")
async def get():
    return {"message": "Hello World"}

# Catch-all route for SPA - must be last
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Don't catch API routes
    if full_path.startswith(SKIP_ROUTES):
        raise HTTPException(status_code=404, detail="Not found")
        
    index_path = PUBLIC_DIR / "index.html"

    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")

    return FileResponse(index_path)