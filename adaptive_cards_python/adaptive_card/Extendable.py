from __future__ import annotations  # Required to defer type hint evaluation!


from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
        str_to_lower=True,
    )


class Item(ConfiguredBaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    requires: dict[str, str] | None = Field(
        default=None,
        description=(
            "A series of key/value pairs indicating features that the item requires"
            " with corresponding minimum version. When a feature is missing or of"
            " insufficient version, fallback is triggered."
        ),
        json_schema_extra={"version": "1.2"},
    )


class ToggleableItem(Item):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: str | None = Field(
        default=None, description="A unique identifier associated with the item."
    )
    isVisible: bool | None = Field(
        default=True,
        description="If `false`, this item will be removed from the visual tree.",
        json_schema_extra={"version": "1.2"},
    )
