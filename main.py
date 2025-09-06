from fastapi import FastAPI

from app.core.config import settings
from app.routers import chat, user

app = FastAPI(
    title=settings.app_name, version=settings.app_version, debug=settings.debug
)


# Include chat router
app.include_router(chat.router, prefix="/api/v1")

# Include users router
app.include_router(user.router, prefix="/api/v1")
