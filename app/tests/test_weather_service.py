from datetime import UTC, datetime, timedelta

import pytest

from app.domain.cache_entry import CacheEntry
from app.domain.weather import Weather


@pytest.mark.asyncio
async def test_get_weather_from_api(weather_service, mock_weather_client, sample_weather):
    result = await weather_service.get_weather("Kyiv")

    assert result.city == "Kyiv"
    assert result.temperature == 20.5
    mock_weather_client.get_weather.assert_called_once_with("Kyiv")


@pytest.mark.asyncio
async def test_get_weather_from_cache(weather_service, cache_repository, mock_weather_client, sample_weather):
    cached_entry = CacheEntry(
        city="kyiv",
        weather=sample_weather,
        cached_at=datetime.now(UTC),
    )
    cache_repository._cache["kyiv"] = cached_entry

    result = await weather_service.get_weather("Kyiv")

    assert result.city == "Kyiv"
    assert result.temperature == 20.5
    mock_weather_client.get_weather.assert_not_called()


@pytest.mark.asyncio
async def test_get_weather_expired_cache(weather_service, cache_repository, mock_weather_client, sample_weather):
    expired_time = datetime.now(UTC) - timedelta(minutes=10)
    cached_entry = CacheEntry(
        city="kyiv",
        weather=sample_weather,
        cached_at=expired_time,
    )
    cache_repository._cache["kyiv"] = cached_entry

    result = await weather_service.get_weather("Kyiv")

    assert result.city == "Kyiv"
    mock_weather_client.get_weather.assert_called_once_with("Kyiv")


@pytest.mark.asyncio
async def test_get_weather_saves_to_storage(weather_service, storage_repository, sample_weather):
    await weather_service.get_weather("Kyiv")

    files = list(storage_repository.data_dir.glob("*.json"))
    assert len(files) == 1
    assert "Kyiv" in files[0].name


@pytest.mark.asyncio
async def test_get_weather_logs_request(weather_service, logging_repository):
    await weather_service.get_weather("Kyiv")

    assert logging_repository.log_file.exists()
    log_content = logging_repository.log_file.read_text()
    assert "Kyiv" in log_content
    assert "success" in log_content


@pytest.mark.asyncio
async def test_get_weather_handles_error(weather_service, mock_weather_client, logging_repository):
    mock_weather_client.get_weather.side_effect = Exception("API Error")

    with pytest.raises(Exception, match="API Error"):
        await weather_service.get_weather("InvalidCity")

    assert logging_repository.log_file.exists()
    log_content = logging_repository.log_file.read_text()
    assert "InvalidCity" in log_content
    assert "error_message" in log_content

