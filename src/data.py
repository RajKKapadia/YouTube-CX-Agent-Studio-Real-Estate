import json
from pathlib import Path

_DATA_PATH = Path(__file__).parent.parent / "data" / "real_estate_dummy_data.json"

with _DATA_PATH.open() as f:
    _raw = json.load(f)

COMPANY: dict = _raw["company"]
PROJECTS: list[dict] = _raw["projects"]
