import pytest
from app.services.file_service import normalize_remote_path

def test_normalize_sdcard_path():
    assert normalize_remote_path("/sdcard/Download") == "/sdcard/Download"

def test_relative_path_is_under_sdcard():
    assert normalize_remote_path("Download") == "/sdcard/Download"

def test_reject_outside_shared_storage():
    with pytest.raises(ValueError):
        normalize_remote_path("/data/data/example")

def test_reject_parent_escape():
    with pytest.raises(ValueError):
        normalize_remote_path("/sdcard/../../data")
