from datetime import UTC, datetime, timedelta

import pytest

from app.domain.cache_entry import CacheEntry
from app.domain.weather import Weather
from app.infrastracture.cache.memory_cache import MemoryCacheRepository


@pytest.mark.asyncio
async def test_cache_set_and_get(cache_repository, sample_weather):
    await cache_repository.set("Kyiv", sample_weather)
    entry = await cache_repository.get("Kyiv")

    assert entry is not None
    assert entry.city == "kyiv"
    assert entry.weather.city == "Kyiv"


@pytest.mark.asyncio
async def test_cache_expired_entry(cache_repository, sample_weather):
    expired_time = datetime.now(UTC) - timedelta(minutes=10)
    cached_entry = CacheEntry(
        city="kyiv",
        weather=sample_weather,
        cached_at=expired_time,
    )
    cache_repository._cache["kyiv"] = cached_entry

    entry = await cache_repository.get("Kyiv")

    assert entry is None
    assert "kyiv" not in cache_repository._cache


@pytest.mark.asyncio
async def test_cache_not_expired_entry(cache_repository, sample_weather):
    recent_time = datetime.now(UTC) - timedelta(minutes=2)
    cached_entry = CacheEntry(
        city="kyiv",
        weather=sample_weather,
        cached_at=recent_time,
    )
    cache_repository._cache["kyiv"] = cached_entry

    entry = await cache_repository.get("Kyiv")

    assert entry is not None
    assert entry.weather.city == "Kyiv"


@pytest.mark.asyncio
async def test_cache_case_insensitive(cache_repository, sample_weather):
    await cache_repository.set("Kyiv", sample_weather)
    entry1 = await cache_repository.get("kyiv")
    entry2 = await cache_repository.get("KYIV")

    assert entry1 is not None
    assert entry2 is not None
    assert entry1.weather.city == entry2.weather.city

