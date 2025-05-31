from __future__ import annotations  # Required to defer type hint evaluation!
from typing import Literal


Spacing = Literal[
    "default", "none", "small", "medium", "large", "extraLarge", "padding"
]
BlockElementHeight = Literal["auto", "stretch"]
FallbackOption = Literal["drop"]
ContainerStyle = Literal[
    "default", "emphasis", "good", "attention", "warning", "accent"
]
FontSize = Literal["default", "small", "medium", "large", "extraLarge"]
FontType = Literal["default", "monospace"]
FontWeight = Literal["default", "lighter", "bolder"]
HorizontalAlignment = Literal["left", "center", "right"]
ImageFillMode = Literal["cover", "repeatHorizontally", "repeatVertically", "repeat"]
ImageSize = Literal["auto", "stretch", "small", "medium", "large"]
ImageStyle = Literal["default", "person"]
TextBlockStyle = Literal["default", "heading"]
VerticalAlignment = Literal["top", "center", "bottom"]
VerticalContentAlignment = Literal["top", "center", "bottom"]
Colors = (
    Literal["default", "dark", "light", "accent", "good", "warning", "attention"] | str
)
