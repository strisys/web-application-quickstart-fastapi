import os, logging, json, uuid, threading
from typing import Optional
from urllib.parse import urlencode
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import identity.web
from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

current_dir = Path(__file__).resolve().parent
dotenv_path = current_dir / '.env'
load_dotenv(dotenv_path)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('msal').setLevel(logging.DEBUG)

router = APIRouter()

class InMemorySessionStore:
    def __init__(self):
        self._sessions: dict[str, dict] = {}
        self._lock = threading.Lock()
        self._last_cleanup = datetime.utcnow()

    def get(self, session_id: str) -> dict:
        with self._lock:
            if (not self.exists(session_id)):
                session_id = str(uuid.uuid4())
                self._sessions[session_id] = {}

            return self._sessions.get(session_id, {})

    def exists(self, session_id: str) -> bool:
        return (self._sessions.get(session_id, None) is not None)
        
    def set(self, session_id: str, data: dict):
        with self._lock:
            self._sessions[session_id] = data

    def cleanup(self, max_age: int = 24 * 60 * 60):
        now = datetime.utcnow()

        if (now - self._last_cleanup) < timedelta(hours=1):
            return
            
        with self._lock:
            for session_id in list(self._sessions.keys()):
                session = self._sessions[session_id]

                if 'last_accessed' in session:
                    last_accessed = datetime.fromisoformat(session['last_accessed'])
                    if (now - last_accessed).total_seconds() > max_age:
                        del self._sessions[session_id]
                        
            self._last_cleanup = now

class AuthSessionMiddleware(BaseHTTPMiddleware):
    AUTH_SESSION_KEY = 'auth_session_id'

    def __init__(self, app):
        super().__init__(app)
        self.session_store = InMemorySessionStore()

    async def dispatch(self, request, call_next):
        session_id = (request.session.get(AuthSessionMiddleware.AUTH_SESSION_KEY) or '')
        auth_session = self.session_store.get(session_id)

        request.state.auth_session = auth_session
        original_session = request.state.auth_session.copy()
        
        response = await call_next(request)

        if request.state.auth_session != original_session:
            self.session_store.set(session_id, request.state.auth_session)
        
        return response
    
class IdentityConfig:
    def __init__(self):
        self.client_id = os.environ.get("AZURE_CLIENT_ID")
        self.client_credential = os.environ.get("AZURE_CLIENT_SECRET") 
        self.authority = f"https://login.microsoftonline.com/{os.environ.get('AZURE_TENANT_ID')}"
        self.redirect_uri = os.environ.get("AZURE_REDIRECT_URI")
        self.scopes = ["https://graph.microsoft.com/.default"]

        if (not self.client_id or not self.client_credential or not self.authority or not self.redirect_uri):
            raise ValueError("Invalid configuration for identity manager.  Expected AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_REDIRECT_URI in environment variables")

class IdentityManager:
    def __init__(self):
        self.config = IdentityConfig()
        
    def get_inner(self, request: Request) -> identity.web.Auth:
        return identity.web.Auth(session=request.state.auth_session, authority=self.config.authority, client_id=self.config.client_id, client_credential=self.config.client_credential)    
    
    def log_in(self, request: Request):
        logger.info("Creating redirect url to log user in")

        inner = self.get_inner(request)
        result = inner.log_in(scopes=self.config.scopes, redirect_uri=self.config.redirect_uri)

        if not "auth_uri" in result:
            logger.info("Failed to create redirect url to log user in")
            raise HTTPException(status_code=500, detail="Failed to initialize login flow")
        
        logger.info("Redirect url to log user in created")
        return RedirectResponse(url=result["auth_uri"])

    def log_out(self, request: Request):
        # self.get_inner(request).log_out(self.config.redirect_uri)
        pass

    def complete_log_in(self, request: Request):
        params = dict(request.query_params)       
        inner = self.get_inner(request)

        logger.info("Exchanging authorization code for token ...")
        result = inner.complete_log_in(params)

        if (len(result) == 0):
            logger.info("Failed to exchange authorization code for token")
            raise HTTPException(status_code=401, detail=result)
        
        logger.info("Authorization cide exchanged for token successfully!")
        return RedirectResponse(url="/", status_code=302)
    
    def get_user(self, request: Request):
        return self.get_inner(request).get_user()

identity_manager = IdentityManager()

@router.route("/login")
async def login(request: Request):   
    return identity_manager.log_in(request)

@router.route("/logout")
def logout(request: Request):
    identity_manager.log_out(request)

@router.get('/signin')
def auth_response(request: Request):
    return identity_manager.complete_log_in(request)

async def authenticate(request: Request, call_next):   
    public_paths = ["/login", "/signin", "/logout"]
    
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)
    
    user = identity_manager.get_user(request)
    logger.info(f"User: {user} accessing resource {request.url.path}")
    
    if (not user):
        return RedirectResponse(url="/login", status_code=302)
    
    return await call_next(request)