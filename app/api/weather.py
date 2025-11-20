from fastapi import APIRouter, Depends, HTTPException

from app.api.dependency import get_weather_service
from app.schemas.weather import WeatherResponse
from app.services.weather_service import WeatherService

router = APIRouter()


@router.get("/", response_model=WeatherResponse)
async def get_weather(
    city: str, service: WeatherService = Depends(get_weather_service)
) -> WeatherResponse:
    try:
        weather = await service.get_weather(city)
        return weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
