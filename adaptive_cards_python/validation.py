from typing import Any

import jsonschema
from pathlib import Path
import json

SCHEMA_URL = "http://adaptivecards.io/schemas/adaptive-card.json"
adaptive_card_json_schema_path = Path(__file__).parent/"adaptive_card/adaptive-card.json"


# class AdaptiveCardModel(BaseModel):
#     """
#     A wrapper model that enforces validation of its entire dict
#     payload against the Adaptive Cards JSON Schema.
#     """
#     __root__: dict

#     @root_validator(pre=True)
#     def enforce_adaptive_schema(cls, values):
#         # Fetch the latest Adaptive Card schema
#         schema = requests.get(SCHEMA_URL).json()
#         # Validate incoming dict against the schema
#         jsonschema.validate(instance=values, schema=schema)
#         return values

def validate_using_json_schema(values: dict[str, Any]):

    with adaptive_card_json_schema_path.open() as outfile:
        schema_json = json.load(outfile)

    jsonschema.validate(instance=values, schema=schema_json)
