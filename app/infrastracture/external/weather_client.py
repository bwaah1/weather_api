from datetime import UTC, datetime

import httpx

from app.domain.weather import Weather


class WeatherAPIClient:
    def __init__(
        self, api_key: str, base_url: str = "https://api.openweathermap.org/data/2.5"
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_weather(self, city: str) -> Weather:
        url = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return Weather(
            city=data["name"],
            temperature=data["main"]["temp"],
            description=data["weather"][0]["description"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=data["wind"]["speed"],
            timestamp=datetime.now(UTC),
            country=data.get("sys", {}).get("country"),
            latitude=data["coord"]["lat"],
            longitude=data["coord"]["lon"],
        )

    async def close(self) -> None:
        await self.client.aclose()
