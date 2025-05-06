from typing import Any

import jsonschema
from pathlib import Path
import json

SCHEMA_URL = "http://adaptivecards.io/schemas/adaptive-card.json"
adaptive_card_json_schema_path: Path = (
    Path(__file__).parent / "adaptive_card/adaptive-card.json"
)


def validate_using_json_schema(values: dict[str, Any]) -> None:
    with adaptive_card_json_schema_path.open() as outfile:
        schema_json = json.load(outfile)

    jsonschema.validate(instance=values, schema=schema_json)
