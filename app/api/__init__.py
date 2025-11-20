from fastapi import APIRouter


def get_router() -> APIRouter:
    from app.api import weather

    router = APIRouter()
    router.include_router(weather.router, prefix="/weather", tags=["weather"])

    return router


__all__ = ["get_router"]
