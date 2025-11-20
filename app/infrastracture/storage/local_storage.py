import json
from datetime import UTC, datetime
from pathlib import Path

from app.domain.repositories.storage import StorageRepository
from app.domain.weather import Weather


class LocalStorageRepository(StorageRepository):
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, city: str, weather: Weather) -> Path:
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"{city}_{timestamp}.json"
        file_path = self.data_dir / filename

        with open(file_path, "w") as f:
            json.dump(weather.model_dump(mode="json"), f, indent=2)

        return file_path
