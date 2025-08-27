"""Tests for EsiFileCache."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest

from eve_argus.eve_argus_esi.esi_cache.esi_cache_protocol import CacheStatus
from eve_argus.eve_argus_esi.esi_cache.esi_file_cache import EsiFileCache
from eve_argus.eve_argus_esi.esi_models import EsiCacheMetadata, EsiResponse


def _mk_response(url: str, cache_key) -> EsiResponse:
    return EsiResponse(
        request_url=url,
        cache_key=cache_key,
        headers=(("Content-Type", "application/json"),),
        text=["body-1"],
    )


def _mk_metadata(
    cache_key, expires: datetime, etag: str = "etag-1"
) -> EsiCacheMetadata:
    now_iso = datetime.now(UTC).isoformat()
    return EsiCacheMetadata(
        cache_key=cache_key,
        expires=expires.astimezone(UTC).isoformat(),
        etag=etag,
        last_modified=now_iso,
        last_checked=now_iso,
    )


def test_get_miss_then_set_and_get_hit_persisted(test_output_dir: Path) -> None:
    """Cache miss then hit after set returns deep-copied data and persists to disk."""
    cache_path = test_output_dir / "esi-cache" / "cache.json"

    key = uuid4()
    resp = _mk_response("https://example.test/1", key)
    meta = _mk_metadata(key, datetime.now(UTC) + timedelta(hours=1))

    # First session: miss then set and hit
    with EsiFileCache(cache_path) as cache:
        assert cache.get(key) is None
        cache.set(key, meta, resp)
        got = cache.get(key)
        assert got is not None
        assert got.cache_key == key
        assert got.response.request_url == resp.request_url
        assert got.metadata.cache_key == key

    # Second session: data persisted
    with EsiFileCache(cache_path) as cache2:
        got2 = cache2.get(key)
        assert got2 is not None
        assert got2.response.request_url == resp.request_url


def test_get_response_and_get_cache_metadata_file(test_output_dir: Path) -> None:
    """Direct getters return deep copies of stored objects and persist across sessions."""
    cache_path = test_output_dir / "esi-cache" / "cache.json"

    key = uuid4()
    resp = _mk_response("https://example.test/2", key)
    meta = _mk_metadata(key, datetime.now(UTC) + timedelta(minutes=5), etag="e2")

    with EsiFileCache(cache_path) as cache:
        cache.set(key, meta, resp)
        got_resp = cache.get_response(key)
        got_meta = cache.get_cache_metadata(key)

        assert got_resp is not None and got_resp.request_url == resp.request_url
        assert got_meta is not None and got_meta.etag == "e2"

    # Re-open and verify again
    with EsiFileCache(cache_path) as cache2:
        got_resp2 = cache2.get_response(key)
        got_meta2 = cache2.get_cache_metadata(key)
        assert got_resp2 is not None and got_resp2.request_url == resp.request_url
        assert got_meta2 is not None and got_meta2.etag == "e2"


def test_clear_and_remove_persist_file(test_output_dir: Path) -> None:
    """Remove one entry and clear all entries; changes persist to file."""
    cache_path = test_output_dir / "esi-cache" / "cache.json"

    key1, key2 = uuid4(), uuid4()

    with EsiFileCache(cache_path) as cache:
        cache.set(
            key1,
            _mk_metadata(key1, datetime.now(UTC) + timedelta(minutes=1)),
            _mk_response("u1", key1),
        )
        cache.set(
            key2,
            _mk_metadata(key2, datetime.now(UTC) + timedelta(minutes=1)),
            _mk_response("u2", key2),
        )

        # remove one
        cache.remove(key1)
        assert cache.get(key1) is None
        assert cache.get(key2) is not None

    # After re-open, key1 still gone, key2 present
    with EsiFileCache(cache_path) as cache2:
        assert cache2.get(key1) is None
        assert cache2.get(key2) is not None

        # clear all
        cache2.clear()
        assert cache2.get(key2) is None

    # After re-open, still empty
    with EsiFileCache(cache_path) as cache3:
        assert cache3.get(key2) is None


def test_status_miss_hit_stale_with_monkeypatch(
    test_output_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Status returns MISS for unknown, HIT for future expiry, STALE for past."""
    cache_path = test_output_dir / "esi-cache" / "cache.json"
    key = uuid4()

    with EsiFileCache(cache_path) as cache:
        # MISS for unknown key
        assert cache.status(key) == CacheStatus.MISS

        # Fix now to a stable point
        fixed_now = datetime(2025, 1, 1, tzinfo=UTC)
        monkeypatch.setattr(
            "eve_argus.eve_argus_esi.esi_cache.esi_file_cache.now_utc",
            lambda: fixed_now,
        )

        # HIT when expires in future
        future = fixed_now + timedelta(minutes=10)
        cache.set(key, _mk_metadata(key, future), _mk_response("u", key))
        assert cache.status(key) == CacheStatus.HIT

        # STALE when expires in past
        past = fixed_now - timedelta(minutes=1)
        cache.set(key, _mk_metadata(key, past), _mk_response("u", key))
        assert cache.status(key) == CacheStatus.STALE


def test_save_creates_directories(test_output_dir: Path) -> None:
    """Saving the cache creates any missing parent directories."""
    cache_path = test_output_dir / "deep" / "nested" / "esi" / "cache.json"
    with EsiFileCache(cache_path):
        # Nothing to set; entering/exiting should create directories and write empty cache
        pass
    assert cache_path.exists() and cache_path.is_file()


def test_save_raises_when_path_is_dir(test_output_dir: Path) -> None:
    """If the cache path is a directory, saving should raise a ValueError."""
    cache_dir_path = test_output_dir / "bad-cache.json"
    cache_dir_path.mkdir(parents=True)
    with pytest.raises(ValueError):
        with EsiFileCache(cache_dir_path):
            # On exit, writing to a directory path should raise
            pass


def test_deepcopy_on_set_and_get_file(test_output_dir: Path) -> None:
    """Cache deep-copies on set and on get to avoid external mutation."""
    cache_path = test_output_dir / "esi-cache" / "cache.json"
    key = uuid4()

    # Original objects
    resp = _mk_response("https://example.test/deep", key)
    meta = _mk_metadata(key, datetime.now(UTC) + timedelta(minutes=2))

    # Keep clean snapshots for comparison
    original_resp = deepcopy(resp)
    original_meta = deepcopy(meta)

    with EsiFileCache(cache_path) as cache:
        # Store (cache should deep copy inputs)
        cache.set(key, meta, resp)

        # Mutate originals after set
        resp.text.append("mutated")
        meta.etag = "mutated-etag"

        # Retrieve and verify stored data unchanged (deep copy on set)
        stored = cache.get(key)
        assert stored is not None
        assert stored.response.text == original_resp.text
        assert stored.metadata.etag == original_meta.etag

        # Mutate returned objects and ensure cache remains unchanged (deep copy on get)
        stored.response.text.append("mutated-2")
        stored.metadata.etag = "mutated-2"

        stored_again = cache.get(key)
        assert stored_again is not None
        assert stored_again.response.text == original_resp.text
        assert stored_again.metadata.etag == original_meta.etag
