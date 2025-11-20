import json
from pathlib import Path

import pytest

from app.infrastracture.storage.local_storage import LocalStorageRepository


@pytest.mark.asyncio
async def test_save_weather_data(storage_repository, sample_weather):
    file_path = await storage_repository.save("Kyiv", sample_weather)

    assert file_path.exists()
    assert "Kyiv" in file_path.name
    assert file_path.suffix == ".json"

    with open(file_path) as f:
        data = json.load(f)
        assert data["city"] == "Kyiv"
        assert data["temperature"] == 20.5


@pytest.mark.asyncio
async def test_save_creates_directory(storage_repository, sample_weather):
    new_dir = storage_repository.data_dir.parent / "new_data"
    new_storage = LocalStorageRepository(data_dir=new_dir)

    await new_storage.save("Kyiv", sample_weather)

    assert new_dir.exists()
    assert (new_dir / "Kyiv_").exists() is False
    files = list(new_dir.glob("*.json"))
    assert len(files) == 1


@pytest.mark.asyncio
async def test_save_filename_format(storage_repository, sample_weather):
    file_path = await storage_repository.save("London", sample_weather)

    assert "London" in file_path.name
    assert "_" in file_path.name
    assert file_path.name.endswith(".json")

