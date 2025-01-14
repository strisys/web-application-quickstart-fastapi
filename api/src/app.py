import os
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
from src.identity_util import configure_pipeline
from dotenv import load_dotenv
import secrets
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
SKIP_ROUTES = ("api/")

app = FastAPI()

configure_pipeline(app)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Static file serving
app.mount("/js", StaticFiles(directory=PUBLIC_DIR / "js"), name="js")
app.mount("/css", StaticFiles(directory=PUBLIC_DIR / "css"), name="css")
app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

@app.get("/manifest.json")
async def serve_manifest():
    return FileResponse(PUBLIC_DIR / "manifest.json")

@app.get("/favicon.ico")
async def serve_favicon():
    return FileResponse(PUBLIC_DIR / "favicon.ico")

@app.get("/robots.txt")
async def serve_robots():
    return FileResponse(PUBLIC_DIR / "robots.txt")

@app.get("/api/hello")
async def get():
    return JSONResponse({"message": "Hello World"})

@app.get("/api/protected")
async def protected_route(request: Request):
    return {"message": "This is a protected route"}

@app.get("/debug-session")
async def debug_session(request: Request):
    request.session["test"] = "hello"
    
    # Log everything
    logger.info(f"Cookies present: {request.cookies}")
    logger.info(f"Session data: {dict(request.session)}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    return {"message": "Session test"}



# Catch-all route for SPA - must be last
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if full_path.startswith(SKIP_ROUTES):
        raise HTTPException(status_code=404, detail="Not found")
        
    index_path = PUBLIC_DIR / "index.html"

    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")

    return FileResponse(index_path)