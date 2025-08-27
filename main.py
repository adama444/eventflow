from fastapi import FastAPI
from app.core.config import settings
from app.core.database import test_connection
from app.core.logger import get_logger
from app.routers import chat

logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name, version=settings.app_version, debug=settings.debug
)


@app.get("/health")
def health_check():
    """
    Simple health check endpoint.
    Returns app and database status.
    """
    try:
        test_connection()
        return {
            "status": "ok",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "database": "connected",
        }
    except Exception as e:
        return {
            "status": "error",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "database": f"connection failed ({str(e)})",
        }


# Include chat router
app.include_router(chat.router, prefix="/api/v1")