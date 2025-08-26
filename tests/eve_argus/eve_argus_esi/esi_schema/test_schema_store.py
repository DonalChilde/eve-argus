"""Tests for SchemaStore context manager and schema loading/saving behavior."""

import json
import tempfile
from pathlib import Path
from uuid import UUID

import pytest

from eve_argus.eve_argus_esi.esi_schema.schema_store import SchemaStore


@pytest.mark.slow
def test_schema_store_real_download():
    """Test that SchemaStore downloads the real ESI schema from the default URL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        schema_path = Path(tmpdir) / "esi_schema.json"
        # Use the default URL from SchemaStore
        assert not schema_path.is_file()
        with SchemaStore(schema_path) as store:
            # store.update_schema()
            # Check that the schema file was written and contains expected keys
            assert schema_path.is_file()
            saved = json.loads(schema_path.read_text())
            assert store.esi_schema is not None
            assert "openapi" in store.esi_schema


def test_schema_store_context_manager_load_and_save(monkeypatch):
    """Test that SchemaStore loads from file, updates, and saves schema."""
    with tempfile.TemporaryDirectory() as tmpdir:
        schema_path = Path(tmpdir) / "esi_schema.json"
        schema_url = "http://dummy-url/schema.json"
        dummy_schema = {"openapi": "3.0.0", "info": {"title": "Dummy"}}
        dummy_json = json.dumps(
            {
                "id_": str(UUID(int=0)),
                "download_date": "2025-08-26T00:00:00Z",
                "schema_": dummy_schema,
            }
        )
        schema_path.write_text(dummy_json)

        def fake_download_text(url):
            return json.dumps({"openapi": "3.0.1", "info": {"title": "Updated"}})

        monkeypatch.setattr(
            "eve_argus.eve_argus_esi.esi_schema.schema_store.download_text",
            fake_download_text,
        )
        monkeypatch.setattr(
            "eve_argus.eve_argus_esi.esi_schema.schema_store.now_utc",
            lambda: type(
                "dt", (), {"isoformat": lambda self: "2025-08-27T00:00:00Z"}
            )(),
        )

        with SchemaStore(schema_path, schema_url) as store:
            assert store.esi_schema["openapi"] == "3.0.0"
            assert store.download_date == "2025-08-26T00:00:00Z"
            assert isinstance(store.schema_id, UUID)
            store.update_schema()
            assert store.esi_schema["openapi"] == "3.0.1"
            assert store.download_date == "2025-08-27T00:00:00Z"

        saved = json.loads(schema_path.read_text())
        assert saved["schema_"]["openapi"] == "3.0.1"
        assert saved["download_date"] == "2025-08-27T00:00:00Z"


def test_schema_store_no_file(monkeypatch):
    """Test that SchemaStore downloads and saves schema if file is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        schema_path = Path(tmpdir) / "esi_schema.json"
        schema_url = "http://dummy-url/schema.json"

        def fake_download_text(url):
            return json.dumps({"openapi": "3.0.1", "info": {"title": "Updated"}})

        monkeypatch.setattr(
            "eve_argus.eve_argus_esi.esi_schema.schema_store.download_text",
            fake_download_text,
        )
        monkeypatch.setattr(
            "eve_argus.eve_argus_esi.esi_schema.schema_store.now_utc",
            lambda: type(
                "dt", (), {"isoformat": lambda self: "2025-08-28T00:00:00Z"}
            )(),
        )
        # File does not exist, so context manager should download and save schema automatically
        assert not schema_path.is_file()
        with SchemaStore(schema_path, schema_url) as store:
            assert schema_path.is_file()
            assert store.esi_schema["openapi"] == "3.0.1"
            assert store.download_date == "2025-08-28T00:00:00Z"
        saved = json.loads(schema_path.read_text())
        assert saved["schema_"]["openapi"] == "3.0.1"
        assert saved["download_date"] == "2025-08-28T00:00:00Z"
