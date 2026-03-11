from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api import authentication, users, fingerprints, locks, logs, device

app = FastAPI(
    title = "Smart Lock API",
    description = "Backend service for a fingerprint-based smart lock system.",
    version = "1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(fingerprints.router)
app.include_router(locks.router)
app.include_router(logs.router)
app.include_router(device.router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}