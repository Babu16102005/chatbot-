from fastapi import FastAPI
from .routers import auth, videos, mcq, progress
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app = FastAPI(title="Career ChatBot API")
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(videos.router, prefix="/api/videos")
app.include_router(mcq.router, prefix="/api/mcq")
app.include_router(progress.router, prefix="/api/progress")

@app.get('/')
def root():
    return {'status':'ok'}
