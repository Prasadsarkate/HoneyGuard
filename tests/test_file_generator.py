from pathlib import Path
from src.core.file_generator import write_honeyfile

def test_write_honeyfile(tmp_path):
    p = tmp_path / "honey"
    path = write_honeyfile(str(p), "test.txt", "abc123")
    assert Path(path).exists()
