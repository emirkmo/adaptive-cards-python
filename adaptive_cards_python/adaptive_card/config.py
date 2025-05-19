from __future__ import annotations  # Required to defer type hint evaluation!
from typing import Literal
from adaptive_cards_python.case_insensitive_literal import CaseInsensitiveLiteral

Spacing = CaseInsensitiveLiteral[
    Literal["default", "none", "small", "medium", "large", "extraLarge", "padding"]
]
BlockElementHeight = CaseInsensitiveLiteral[Literal["auto", "stretch"]]
FallbackOption = CaseInsensitiveLiteral[Literal["drop"]]
ContainerStyle = CaseInsensitiveLiteral[
    Literal["default", "emphasis", "good", "attention", "warning", "accent"]
]
FontSize = CaseInsensitiveLiteral[
    Literal["default", "small", "medium", "large", "extraLarge"]
]
FontType = CaseInsensitiveLiteral[Literal["default", "monospace"]]
FontWeight = CaseInsensitiveLiteral[Literal["default", "lighter", "bolder"]]
HorizontalAlignment = CaseInsensitiveLiteral[Literal["left", "center", "right"]]
ImageFillMode = CaseInsensitiveLiteral[
    Literal["cover", "repeatHorizontally", "repeatVertically", "repeat"]
]
ImageSize = CaseInsensitiveLiteral[
    Literal["auto", "stretch", "small", "medium", "large"]
]
ImageStyle = CaseInsensitiveLiteral[Literal["default", "person"]]
TextBlockStyle = CaseInsensitiveLiteral[Literal["default", "heading"]]
VerticalAlignment = CaseInsensitiveLiteral[Literal["top", "center", "bottom"]]
VerticalContentAlignment = CaseInsensitiveLiteral[Literal["top", "center", "bottom"]]
Colors = (
    (
        CaseInsensitiveLiteral[
            Literal[
                "default", "dark", "light", "accent", "good", "warning", "attention"
            ]
        ]
    )
    | str
)
