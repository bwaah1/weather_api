from fastapi import Request

from app.services.weather_service import WeatherService


def get_weather_service(request: Request) -> WeatherService:
    return request.app.state.weather_service  # type: ignore[no-any-return]
