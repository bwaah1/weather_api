import json
from datetime import UTC, datetime

import pytest

from app.domain.weather_log import WeatherLog
from app.infrastracture.logging.local_logging import LocalLoggingRepository


@pytest.mark.asyncio
async def test_log_entry(logging_repository):
    log_entry = WeatherLog(
        city="Kyiv",
        timestamp=datetime.now(UTC),
        file_path="/data/Kyiv_20240101_120000.json",
        success=True,
    )

    await logging_repository.log(log_entry)

    assert logging_repository.log_file.exists()
    content = logging_repository.log_file.read_text()
    assert "Kyiv" in content
    assert "success" in content


@pytest.mark.asyncio
async def test_log_multiple_entries(logging_repository):
    entry1 = WeatherLog(
        city="Kyiv",
        timestamp=datetime.now(UTC),
        file_path="/data/kyiv.json",
        success=True,
    )
    entry2 = WeatherLog(
        city="London",
        timestamp=datetime.now(UTC),
        file_path="/data/london.json",
        success=True,
    )

    await logging_repository.log(entry1)
    await logging_repository.log(entry2)

    lines = logging_repository.log_file.read_text().strip().split("\n")
    assert len(lines) == 2
    assert "Kyiv" in lines[0]
    assert "London" in lines[1]


@pytest.mark.asyncio
async def test_log_error_entry(logging_repository):
    log_entry = WeatherLog(
        city="InvalidCity",
        timestamp=datetime.now(UTC),
        file_path="",
        success=False,
        error_message="City not found",
    )

    await logging_repository.log(log_entry)

    content = logging_repository.log_file.read_text()
    data = json.loads(content)
    assert data["success"] is False
    assert data["error_message"] == "City not found"


@pytest.mark.asyncio
async def test_log_creates_directory(logging_repository):
    new_log_file = logging_repository.log_file.parent.parent / "new_logs" / "test.log"
    new_logging = LocalLoggingRepository(log_file=new_log_file)

    entry = WeatherLog(
        city="Test",
        timestamp=datetime.now(UTC),
        file_path="",
        success=True,
    )

    await new_logging.log(entry)

    assert new_log_file.parent.exists()
    assert new_log_file.exists()

