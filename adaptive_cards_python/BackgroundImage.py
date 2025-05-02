from __future__ import annotations  # Required to defer type hint evaluation!
from pydantic import Field
from .config import ImageFillMode, HorizontalAlignment, VerticalAlignment
from .Extendable import ConfiguredBaseModel

from typing import Literal


class BackgroundImage(ConfiguredBaseModel):
    """
    Specifies a background image. Acceptable formats are PNG, JPEG, and GIF
    """

    type: Literal["BackgroundImage"] = Field(
        default="BackgroundImage", description="Must be `BackgroundImage`"
    )
    url: str = Field(
        ...,
        description=(
            "The URL (or data url) of the image. Acceptable formats are PNG, JPEG,"
            " and GIF"
        ),
    )
    fillMode: ImageFillMode | None = Field(
        default=None, description="Describes how the image should fill the area."
    )
    horizontalAlignment: HorizontalAlignment | None = Field(
        default=None,
        description=(
            "Describes how the image should be aligned if it must be cropped or if"
            " using repeat fill mode."
        ),
    )
    verticalAlignment: VerticalAlignment | None = Field(
        default=None,
        description=(
            "Describes how the image should be aligned if it must be cropped or if"
            " using repeat fill mode."
        ),
    )
