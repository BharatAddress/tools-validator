from pathlib import Path
import subprocess


def test_validate_collection_ok(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    data = repo_root / "data" / "sample.geojson"
    schema = repo_root / "specs" / "address-register.schema.json"
    result = subprocess.run([
        "python",
        str(repo_root / "validate.py"),
        str(data),
        "--schema",
        str(schema),
        "--schema-target",
        "collection",
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
