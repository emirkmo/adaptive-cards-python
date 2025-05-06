from __future__ import annotations  # Required to defer type hint evaluation!
from pydantic import Field, ConfigDict

from typing import Annotated, Literal, Self

from .BackgroundImage import BackgroundImage
from .Extendable import ToggleableItem, ConfiguredBaseModel
from .config import (
    Colors,
    FallbackOption,
    BlockElementHeight,
    FontSize,
    FontType,
    FontWeight,
    HorizontalAlignment,
    ImageSize,
    Spacing,
    ContainerStyle,
    TextBlockStyle,
    VerticalAlignment,
    VerticalContentAlignment,
    ImageStyle,
)
from .Action import ActionType, ISelectActionType


class Element(ToggleableItem):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    fallback: ElementType | FallbackOption = Field(
        default="drop",
        description=(
            "Describes what to do when an unknown element is encountered or the"
            " requires of this or any children can't be met."
        ),
        json_schema_extra={"version": "1.2"},
    )
    height: BlockElementHeight | None = Field(
        default=None,
        description="Specifies the height of the element.",
        json_schema_extra={"version": "1.1"},
    )
    separator: bool | None = Field(
        default=None,
        description="When `true`, draw a separating line at the top of the element.",
    )
    spacing: Spacing | None = Field(
        default=None,
        description=(
            "Controls the amount of spacing between this element and the preceding"
            " element."
        ),
    )


class ActionSet(Element):
    """
    Displays a set of actions.
    """

    type: Literal["ActionSet"] = Field(
        default="ActionSet", description="Must be `ActionSet`"
    )
    actions: list[ActionType] = Field(
        ..., description="The array of `Action` elements to show."
    )


class Column(ToggleableItem):
    """
    Defines a container that is part of a ColumnSet.
    """

    type: Literal["Column"] = Field(default="Column", description="Must be `Column`")
    items: list[ElementType] | None = Field(
        default=None, description="The card elements to render inside the `Column`."
    )
    backgroundImage: BackgroundImage | str | None = Field(
        default=None,
        description=(
            "Specifies the background image. Acceptable formats are PNG, JPEG, and GIF"
        ),
        json_schema_extra={"version": "1.2"},
    )
    bleed: bool | None = Field(
        default=None,
        description=(
            "Determines whether the column should bleed through its parent's padding."
        ),
        json_schema_extra={"version": "1.2", "features": [2109]},
    )
    fallback: Self | FallbackOption | None = Field(
        default=None,
        description=(
            "Describes what to do when an unknown item is encountered or the requires"
            " of this or any children can't be met."
        ),
        json_schema_extra={"version": "1.2"},
    )
    minHeight: str | None = Field(
        default=None,
        description=(
            'Specifies the minimum height of the column in pixels, like `"80px"`.'
        ),
        examples=["50px"],
        json_schema_extra={"version": "1.2", "features": [2293]},
    )
    rtl: bool | None = Field(
        default=None,
        description=(
            "When `true` content in this column should be presented right to left. When"
            " 'false' content in this column should be presented left to right. When"
            " unset layout direction will inherit from parent container or column. If"
            " unset in all ancestors, the default platform behavior will apply."
        ),
        json_schema_extra={"version": "1.5"},
    )
    separator: bool | None = Field(
        default=None,
        description=(
            "When `true`, draw a separating line between this column and the previous"
            " column."
        ),
    )
    spacing: Spacing | None = Field(
        default=None,
        description=(
            "Controls the amount of spacing between this column and the preceding"
            " column."
        ),
    )
    selectAction: ISelectActionType | None = Field(
        default=None,
        description=(
            "An Action that will be invoked when the `Column` is tapped or selected."
            " `Action.ShowCard` is not supported."
        ),
        json_schema_extra={"version": "1.1"},
    )
    style: ContainerStyle | None = Field(
        default=None, description="Style hint for `Column`."
    )
    verticalContentAlignment: VerticalContentAlignment | None = Field(
        default=None,
        description=(
            "Defines how the content should be aligned vertically within the column."
            " When not specified, the value of verticalContentAlignment is inherited"
            " from the parent container. If no parent container has"
            " verticalContentAlignment set, it defaults to Top."
        ),
        json_schema_extra={"version": "1.1"},
    )
    width: str | float | None = Field(
        default=None,
        description=(
            '`"auto"`, `"stretch"`, a number representing relative width of the column'
            " in the column group, or in version 1.1 and higher, a specific pixel"
            ' width, like `"50px"`.'
        ),
    )


class ColumnSet(Element):
    """
    ColumnSet divides a region into Columns, allowing elements to sit side-by-side.
    """

    type: Literal["ColumnSet"] = Field(
        default="ColumnSet", description="Must be `ColumnSet`"
    )
    columns: list[Column] | None = Field(
        default=None, description="The array of `Columns` to divide the region into."
    )
    selectAction: ISelectActionType | None = Field(
        default=None,
        description=(
            "An Action that will be invoked when the `ColumnSet` is tapped or selected."
            " `Action.ShowCard` is not supported."
        ),
        json_schema_extra={"version": "1.1"},
    )
    style: ContainerStyle | None = Field(
        default=None,
        description="Style hint for `ColumnSet`.",
        json_schema_extra={"version": "1.2"},
    )
    bleed: bool | None = Field(
        default=None,
        description=(
            "Determines whether the element should bleed through its parent's padding."
        ),
        json_schema_extra={"version": "1.2", "features": [2109]},
    )
    minHeight: str | None = Field(
        default=None,
        description=(
            'Specifies the minimum height of the column set in pixels, like `"80px"`.'
        ),
        examples=["50px"],
        json_schema_extra={"version": "1.2", "features": [2293]},
    )
    horizontalAlignment: HorizontalAlignment | None = Field(
        default=None,
        description=(
            "Controls the horizontal alignment of the ColumnSet. When not specified,"
            " the value of horizontalAlignment is inherited from the parent container."
            " If no parent container has horizontalAlignment set, it defaults to Left."
        ),
    )


class Container(Element):
    """
    Containers group items together.
    """

    type: Literal["Container"] = Field(
        default="Container", description="Must be `Container`"
    )
    items: list[ElementType] = Field(
        ..., description="The card elements to render inside the `Container`."
    )
    selectAction: ISelectActionType | None = Field(
        default=None,
        description=(
            "An Action that will be invoked when the `Container` is tapped or selected."
            " `Action.ShowCard` is not supported."
        ),
        json_schema_extra={"version": "1.1"},
    )
    style: ContainerStyle | None = Field(
        default=None, description="Style hint for `Container`."
    )
    verticalContentAlignment: VerticalContentAlignment | None = Field(
        default=None,
        description=(
            "Defines how the content should be aligned vertically within the container."
            " When not specified, the value of verticalContentAlignment is inherited"
            " from the parent container. If no parent container has"
            " verticalContentAlignment set, it defaults to Top."
        ),
        json_schema_extra={"version": "1.1"},
    )
    bleed: bool | None = Field(
        default=None,
        description=(
            "Determines whether the element should bleed through its parent's padding."
        ),
        json_schema_extra={"version": "1.2", "features": [2109]},
    )
    backgroundImage: BackgroundImage | str | None = Field(
        default=None,
        description=(
            "Specifies the background image. Acceptable formats are PNG, JPEG, and GIF"
        ),
        json_schema_extra={"version": "1.2"},
    )
    minHeight: str | None = Field(
        default=None,
        description=(
            'Specifies the minimum height of the container in pixels, like `"80px"`.'
        ),
        examples=["50px"],
        json_schema_extra={"version": "1.2", "features": [2293]},
    )
    rtl_: bool | None = Field(
        default=None,
        alias="rtl?",
        description=(
            "When `true` content in this container should be presented right to left."
            " When 'false' content in this container should be presented left to right."
            " When unset layout direction will inherit from parent container or column."
            " If unset in all ancestors, the default platform behavior will apply."
        ),
        json_schema_extra={"version": "1.5"},
    )


class Fact(ConfiguredBaseModel):
    """
    Describes a Fact in a FactSet as a key/value pair.
    """

    type: Literal["Fact"] = Field(default="Fact", description="Must be `Fact`")
    title: str = Field(..., description="The title of the fact.")
    value: str = Field(..., description="The value of the fact.")


class FactSet(Element):
    """
    The FactSet element displays a series of facts (i.e. name/value pairs) in a tabular form.
    """

    type: Literal["FactSet"] = Field(default="FactSet", description="Must be `FactSet`")
    facts: list[Fact] = Field(..., description="The array of `Fact`'s.")


class Image(ConfiguredBaseModel):
    """
    Displays an image. Acceptable formats are PNG, JPEG, and GIF
    """

    type: Literal["Image"] = Field(default="Image", description="Must be `Image`")
    url: str = Field(
        ..., description="The URL to the image. Supports data URI in version 1.2+"
    )
    altText: str | None = Field(
        default=None, description="Alternate text describing the image."
    )
    backgroundColor: str | None = Field(
        default=None,
        description=(
            "Applies a background to a transparent image. This property will respect"
            " the image style."
        ),
        examples=["#DDDDDD"],
        json_schema_extra={"version": "1.1"},
    )
    height: str | BlockElementHeight | None = Field(
        default="auto",
        description=(
            "The desired height of the image. If specified as a pixel value, ending in"
            " 'px', E.g., 50px, the image will distort to fit that exact height. This"
            " overrides the `size` property."
        ),
        examples=["50px"],
        json_schema_extra={"version": "1.1"},
    )
    horizontalAlignment: HorizontalAlignment | None = Field(
        default=None,
        description=(
            "Controls how this element is horizontally positioned within its parent."
            " When not specified, the value of horizontalAlignment is inherited from"
            " the parent container. If no parent container has horizontalAlignment set,"
            " it defaults to Left."
        ),
    )
    selectAction: ISelectActionType | None = Field(
        default=None,
        description=(
            "An Action that will be invoked when the `Image` is tapped or selected."
            " `Action.ShowCard` is not supported."
        ),
        json_schema_extra={"version": "1.1"},
    )
    size: ImageSize | None = Field(
        default=None,
        description=(
            "Controls the approximate size of the image. The physical dimensions will"
            " vary per host."
        ),
    )
    style: ImageStyle | None = Field(
        default=None, description="Controls how this `Image` is displayed."
    )
    width: str | None = Field(
        default=None,
        description=(
            "The desired on-screen width of the image, ending in 'px'. E.g., 50px. This"
            " overrides the `size` property."
        ),
        examples=["50px"],
        json_schema_extra={"version": "1.1"},
    )
    fallback: ElementType | FallbackOption | None = Field(
        default=None,
        description=(
            "Describes what to do when an unknown element is encountered or the"
            " requires of this or any children can't be met."
        ),
        json_schema_extra={"version": "1.2"},
    )
    separator: bool | None = Field(
        default=None,
        description="When `true`, draw a separating line at the top of the element.",
    )
    spacing: Spacing | None = Field(
        default=None,
        description=(
            "Controls the amount of spacing between this element and the preceding"
            " element."
        ),
    )
    id: str | None = Field(
        default=None, description="A unique identifier associated with the item."
    )
    isVisible: bool | None = Field(
        default=True,
        description="If `false`, this item will be removed from the visual tree.",
        json_schema_extra={"version": "1.2"},
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


class ImageSet(Element):
    """
    The ImageSet displays a collection of Images similar to a gallery. Acceptable formats are PNG, JPEG, and GIF
    """

    type: Literal["ImageSet"] = Field(
        default="ImageSet", description="Must be `ImageSet`"
    )
    images: list[Image] = Field(
        ..., description="The array of `Image` elements to show."
    )
    imageSize: ImageSize | None = Field(
        default="medium",
        description=(
            "Controls the approximate size of each image. The physical dimensions will"
            " vary per host. Auto and stretch are not supported for ImageSet. The size"
            " will default to medium if those values are set."
        ),
    )


class MediaSource(ConfiguredBaseModel):
    """
    Defines a source for a Media element
    """

    type: Literal["MediaSource"] = Field(
        default="MediaSource", description="Must be `MediaSource`"
    )
    mimeType: str = Field(
        ..., description='Mime type of associated media (e.g. `"video/mp4"`).'
    )
    url: str = Field(..., description="URL to media. Supports data URI in version 1.2+")


class Media(Element):
    """
    Displays a media player for audio or video content.
    """

    type: Literal["Media"] = Field(default="Media", description="Must be `Media`")
    sources: list[MediaSource] = Field(
        ..., description="Array of media sources to attempt to play."
    )
    poster: str | None = Field(
        default=None,
        description=(
            "URL of an image to display before playing. Supports data URI in version"
            " 1.2+"
        ),
    )
    altText: str | None = Field(
        default=None, description="Alternate text describing the audio or video."
    )


class TextRun(ConfiguredBaseModel):
    """
    Defines a single run of formatted text.
    A TextRun with no properties set can be represented in the json as string containing the text
    as a shorthand for the json object. These two representations are equivalent.
    """

    type: Literal["TextRun"] = Field(default="TextRun", description="Must be `TextRun`")
    text: str = Field(..., description="Text to display. Markdown is not supported.")
    color: Colors | None = Field(
        default=None, description="Controls the color of the text."
    )
    fontType: FontType | None = Field(
        default=None, description="The type of font to use"
    )
    highlight: bool | None = Field(
        default=None, description="If `true`, displays the text highlighted."
    )
    isSubtle: bool | None = Field(
        default=False,
        description=(
            "If `true`, displays text slightly toned down to appear less prominent."
        ),
    )
    italic: bool | None = Field(
        default=None, description="If `true`, displays the text using italic font."
    )
    selectAction: ISelectActionType | None = Field(
        default=None,
        description=(
            "Action to invoke when this text run is clicked. Visually changes the text"
            " run into a hyperlink. `Action.ShowCard` is not supported."
        ),
    )
    size: FontSize | None = Field(default=None, description="Controls size of text.")
    strikethrough: bool | None = Field(
        default=None, description="If `true`, displays the text with strikethrough."
    )
    underline: bool | None = Field(
        default=None, description="If `true`, displays the text with an underline."
    )
    weight: FontWeight | None = Field(
        default=None, description="Controls the weight of the text."
    )


class RichTextBlock(Element):
    """
    Defines an array of inlines, allowing for inline text formatting.
    """

    type: Literal["RichTextBlock"] = Field(
        default="RichTextBlock", description="Must be `RichTextBlock`"
    )
    inlines: list[TextRun | str] = Field(..., description="The array of inlines.")
    horizontalAlignment: HorizontalAlignment | None = Field(
        default=None,
        description=(
            "Controls the horizontal text alignment. When not specified, the value of"
            " horizontalAlignment is inherited from the parent container. If no parent"
            " container has horizontalAlignment set, it defaults to Left."
        ),
    )


class TableColumnDefinition(ConfiguredBaseModel):
    """
    Defines the characteristics of a column in a Table element.
    """

    type: Literal["TableColumnDefinition"] = Field(
        default="TableColumnDefinition", description="Must be `TableColumnDefinition`"
    )
    width: str | float | None = Field(
        default=1,
        description=(
            "Specifies the width of the column. If expressed as a number, width"
            " represents the weight a the column relative to the other columns in the"
            ' table. If expressed as a string, width must by in the format "<number>px"'
            ' (for instance, "50px") and represents an explicit number of pixels.'
        ),
    )
    horizontalCellContentAlignment: HorizontalAlignment | None = Field(
        default=None,
        description=(
            "Controls how the content of all cells in the column is horizontally"
            " aligned by default. When specified, this value overrides the setting at"
            " the table level. When not specified, horizontal alignment is defined at"
            " the table, row or cell level."
        ),
    )
    verticalCellContentAlignment: VerticalAlignment | None = Field(
        default=None,
        description=(
            "Controls how the content of all cells in the column is vertically aligned"
            " by default. When specified, this value overrides the setting at the table"
            " level. When not specified, vertical alignment is defined at the table,"
            " row or cell level."
        ),
    )


class TableCell(ConfiguredBaseModel):
    """
    Represents a cell within a row of a Table element.
    """

    type: Literal["TableCell"] = Field(
        default="TableCell", description="Must be `TableCell`"
    )
    items: list[ElementType] = Field(
        ..., description="The card elements to render inside the `TableCell`."
    )
    selectAction: ISelectActionType | None = Field(
        default=None,
        description=(
            "An Action that will be invoked when the `TableCell` is tapped or selected."
            " `Action.ShowCard` is not supported."
        ),
        json_schema_extra={"version": "1.1"},
    )
    style: ContainerStyle | None = Field(
        default=None, description="Style hint for `TableCell`."
    )
    verticalContentAlignment: VerticalContentAlignment | None = Field(
        default=None,
        description=(
            "Defines how the content should be aligned vertically within the container."
            " When not specified, the value of verticalContentAlignment is inherited"
            " from the parent container. If no parent container has"
            " verticalContentAlignment set, it defaults to Top."
        ),
        json_schema_extra={"version": "1.1"},
    )
    bleed: bool | None = Field(
        default=None,
        description=(
            "Determines whether the element should bleed through its parent's padding."
        ),
        json_schema_extra={"version": "1.2", "features": [2109]},
    )
    backgroundImage: BackgroundImage | str | None = Field(
        default=None,
        description=(
            "Specifies the background image. Acceptable formats are PNG, JPEG, and GIF"
        ),
        json_schema_extra={"version": "1.2"},
    )
    minHeight: str | None = Field(
        default=None,
        description=(
            'Specifies the minimum height of the container in pixels, like `"80px"`.'
        ),
        examples=["50px"],
        json_schema_extra={"version": "1.2", "features": [2293]},
    )
    rtl_: bool | None = Field(
        default=None,
        alias="rtl?",
        description=(
            "When `true` content in this container should be presented right to left."
            " When 'false' content in this container should be presented left to right."
            " When unset layout direction will inherit from parent container or column."
            " If unset in all ancestors, the default platform behavior will apply."
        ),
        json_schema_extra={"version": "1.5"},
    )


class TableRow(ConfiguredBaseModel):
    """
    Represents a row of cells within a Table element.
    """

    type: Literal["TableRow"] = Field(
        default="TableRow", description="Must be `TableRow`"
    )
    cells: list[TableCell] | None = Field(
        default=None,
        description=(
            "The cells in this row. If a row contains more cells than there are columns"
            " defined on the Table element, the extra cells are ignored."
        ),
    )
    style: ContainerStyle | None = Field(
        default=None, description="Defines the style of the entire row."
    )
    horizontalCellContentAlignment: HorizontalAlignment | None = Field(
        default=None,
        description=(
            "Controls how the content of all cells in the row is horizontally aligned"
            " by default. When specified, this value overrides both the setting at the"
            " table and columns level. When not specified, horizontal alignment is"
            " defined at the table, column or cell level."
        ),
    )
    verticalCellContentAlignment: VerticalAlignment | None = Field(
        default=None,
        description=(
            "Controls how the content of all cells in the column is vertically aligned"
            " by default. When specified, this value overrides the setting at the table"
            " and column level. When not specified, vertical alignment is defined"
            " either at the table, column or cell level."
        ),
    )


class Table(Element):
    """
    Provides a way to display data in a tabular form.
    """

    type: Literal["Table"] = Field(default="Table", description="Must be `Table`")
    columns: list[TableColumnDefinition] | None = Field(
        default=None,
        description=(
            "Defines the number of columns in the table, their sizes, and more."
        ),
    )
    rows: list[TableRow] | None = Field(
        default=None, description="Defines the rows of the table."
    )
    firstRowAsHeader: bool | None = Field(
        default=True,
        description=(
            "Specifies whether the first row of the table should be treated as a header"
            " row, and be announced as such by accessibility software."
        ),
    )
    showGridLines: bool | None = Field(
        default=True, description="Specifies whether grid lines should be displayed."
    )
    gridStyle: ContainerStyle | None = Field(
        default="default",
        description=(
            "Defines the style of the grid. This property currently only controls the"
            " grid's color."
        ),
    )
    horizontalCellContentAlignment: HorizontalAlignment | None = Field(
        default=None,
        description=(
            "Controls how the content of all cells is horizontally aligned by default."
            " When not specified, horizontal alignment is defined on a per-cell basis."
        ),
    )
    verticalCellContentAlignment: VerticalAlignment | None = Field(
        default=None,
        description=(
            "Controls how the content of all cells is vertically aligned by default."
            " When not specified, vertical alignment is defined on a per-cell basis."
        ),
    )


class TextBlock(Element):
    """
    Displays text, allowing control over font sizes, weight, and color.
    """

    type: Literal["TextBlock"] = Field(
        default="TextBlock", description="Must be `TextBlock`"
    )
    text: str = Field(
        ...,
        description=(
            "Text to display. A subset of markdown is supported"
            " (https://aka.ms/ACTextFeatures)"
        ),
    )
    color: Colors | None = Field(
        default=None, description="Controls the color of `TextBlock` elements."
    )
    fontType: FontType | None = Field(
        default=None,
        description="Type of font to use for rendering",
        json_schema_extra={"version": "1.2"},
    )
    horizontalAlignment: HorizontalAlignment | None = Field(
        default=None,
        description=(
            "Controls the horizontal text alignment. When not specified, the value of"
            " horizontalAlignment is inherited from the parent container. If no parent"
            " container has horizontalAlignment set, it defaults to Left."
        ),
    )
    isSubtle: bool | None = Field(
        default=False,
        description=(
            "If `true`, displays text slightly toned down to appear less prominent."
        ),
    )
    maxLines: float | None = Field(
        default=None, description="Specifies the maximum number of lines to display."
    )
    size: FontSize | None = Field(default=None, description="Controls size of text.")
    weight: FontWeight | None = Field(
        default=None, description="Controls the weight of `TextBlock` elements."
    )
    wrap: bool | None = Field(
        default=False,
        description="If `true`, allow text to wrap. Otherwise, text is clipped.",
    )
    style: TextBlockStyle | None = Field(
        default="default",
        description="The style of this TextBlock for accessibility purposes.",
    )


class Input(ConfiguredBaseModel):
    """
    Base input class
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: str = Field(
        ...,
        description=(
            "Unique identifier for the value. Used to identify collected input when the"
            " Submit action is performed."
        ),
    )
    errorMessage: str | None = Field(
        default=None,
        description="Error message to display when entered input is invalid",
        json_schema_extra={"version": "1.3"},
    )
    isRequired: bool | None = Field(
        default=None,
        description="Whether or not this input is required",
        json_schema_extra={"version": "1.3"},
    )
    label: str | None = Field(
        default=None,
        description="Label for this input",
        json_schema_extra={"version": "1.3"},
    )
    fallback: ElementType | FallbackOption | None = Field(
        default=None,
        description=(
            "Describes what to do when an unknown element is encountered or the"
            " requires of this or any children can't be met."
        ),
        json_schema_extra={"version": "1.2"},
    )
    height: BlockElementHeight | None = Field(
        default=None,
        description="Specifies the height of the element.",
        json_schema_extra={"version": "1.1"},
    )
    separator: bool | None = Field(
        default=None,
        description="When `true`, draw a separating line at the top of the element.",
    )
    spacing: Spacing | None = Field(
        default=None,
        description=(
            "Controls the amount of spacing between this element and the preceding"
            " element."
        ),
    )
    isVisible: bool | None = Field(
        default=True,
        description="If `false`, this item will be removed from the visual tree.",
        json_schema_extra={"version": "1.2"},
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


class Choice(ConfiguredBaseModel):
    """
    Describes a choice for use in a ChoiceSet.
    """

    type: Literal["Input.Choice"] = Field(
        default="Input.Choice", description="Must be `Input.Choice`"
    )
    title: str = Field(..., description="Text to display.")
    value: str = Field(
        ...,
        description=(
            "The raw value for the choice. **NOTE:** do not use a `,` in the value,"
            " since a `ChoiceSet` with `isMultiSelect` set to `true` returns a"
            " comma-delimited string of choice values."
        ),
    )


ChoiceInputStyle = Literal["compact", "expanded"]


class ChoiceSet(Input):
    """
    Allows a user to input a Choice.
    """

    type: Literal["Input.ChoiceSet"] = Field(
        default="Input.ChoiceSet", description="Must be `Input.ChoiceSet`"
    )
    choices: list[Choice] | None = Field(default=None, description="`Choice` options.")
    isMultiSelect: bool | None = Field(
        default=False, description="Allow multiple choices to be selected."
    )
    style: ChoiceInputStyle | None = None
    value: str | None = Field(
        default=None,
        description=(
            "The initial choice (or set of choices) that should be selected. For"
            " multi-select, specify a comma-separated string of values."
        ),
    )
    placeholder: str | None = Field(
        default=None,
        description=(
            "Description of the input desired. Only visible when no selection has been"
            " made, the `style` is `compact` and `isMultiSelect` is `false`"
        ),
    )
    wrap: bool | None = Field(
        default=None,
        description="If `true`, allow text to wrap. Otherwise, text is clipped.",
        json_schema_extra={"version": "1.2"},
    )


class Date(Input):
    """
    Lets a user choose a date.
    """

    type: Literal["Input.Date"] = Field(
        default="Input.Date", description="Must be `Input.Date`"
    )
    max: str | None = Field(
        default=None,
        description=(
            "Hint of maximum value expressed in YYYY-MM-DD(may be ignored by some"
            " clients)."
        ),
    )
    min: str | None = Field(
        default=None,
        description=(
            "Hint of minimum value expressed in YYYY-MM-DD(may be ignored by some"
            " clients)."
        ),
    )
    placeholder: str | None = Field(
        default=None,
        description=(
            "Description of the input desired. Displayed when no selection has been"
            " made."
        ),
    )
    value: str | None = Field(
        default=None,
        description="The initial value for this field expressed in YYYY-MM-DD.",
    )


class Number(Input):
    """
    Allows a user to enter a number.
    """

    type: Literal["Input.Number"] = Field(
        default="Input.Number", description="Must be `Input.Number`"
    )
    max: float | None = Field(
        default=None,
        description="Hint of maximum value (may be ignored by some clients).",
    )
    min: float | None = Field(
        default=None,
        description="Hint of minimum value (may be ignored by some clients).",
    )
    placeholder: str | None = Field(
        default=None,
        description=(
            "Description of the input desired. Displayed when no selection has been"
            " made."
        ),
    )
    value: float | None = Field(
        default=None, description="Initial value for this field."
    )


TextInputStyle = Literal["text", "tel", "url", "email", "password"]


class Text(Input):
    """
    Lets a user enter text.
    """

    type: Literal["Input.Text"] = Field(
        default="Input.Text", description="Must be `Input.Text`"
    )
    isMultiline: bool | None = Field(
        default=False, description="If `true`, allow multiple lines of input."
    )
    maxLength: float | None = Field(
        default=None,
        description=(
            "Hint of maximum length characters to collect (may be ignored by some"
            " clients)."
        ),
    )
    placeholder: str | None = Field(
        default=None,
        description=(
            "Description of the input desired. Displayed when no text has been input."
        ),
    )
    regex: str | None = Field(
        default=None,
        description=(
            "Regular expression indicating the required format of this text input."
        ),
        json_schema_extra={"version": "1.3"},
    )
    style: TextInputStyle | None = Field(
        default=None, description="Style hint for text input."
    )
    inlineAction: ActionType | None = Field(
        default=None,
        description=(
            "The inline action for the input. Typically displayed to the right of the"
            " input. It is strongly recommended to provide an icon on the action (which"
            " will be displayed instead of the title of the action)."
        ),
        json_schema_extra={"version": "1.2"},
    )
    value: str | None = Field(
        default=None, description="The initial value for this field."
    )


class Time(Input):
    """
    Lets a user select a time.
    """

    type: Literal["Input.Time"] = Field(
        default="Input.Time", description="Must be `Input.Time`"
    )
    max: str | None = Field(
        default=None,
        description=(
            "Hint of maximum value expressed in HH:MM (may be ignored by some clients)."
        ),
    )
    min: str | None = Field(
        default=None,
        description=(
            "Hint of minimum value expressed in HH:MM (may be ignored by some clients)."
        ),
    )
    placeholder: str | None = Field(
        default=None,
        description=(
            "Description of the input desired. Displayed when no time has been"
            " selected."
        ),
    )
    value: str | None = Field(
        default=None, description="The initial value for this field expressed in HH:MM."
    )


class Toggle(Input):
    """
    Lets a user choose between two options.
    """

    type: Literal["Input.Toggle"] = Field(
        default="Input.Toggle", description="Must be `Input.Toggle`"
    )
    title: str = Field(..., description="Title for the toggle")
    value: str | None = Field(
        default="false",
        description=(
            "The initial selected value. If you want the toggle to be initially on, set"
            " this to the value of `valueOn`'s value."
        ),
    )
    valueOff: str | None = Field(
        default="false", description="The value when toggle is off"
    )
    valueOn: str | None = Field(
        default="true", description="The value when toggle is on"
    )
    wrap: bool | None = Field(
        default=None,
        description="If `true`, allow text to wrap. Otherwise, text is clipped.",
        json_schema_extra={"version": "1.2"},
    )


ElementType = Annotated[
    ActionSet
    | ColumnSet
    | Container
    | FactSet
    | Image
    | ImageSet
    | Media
    | RichTextBlock
    | Table
    | TextBlock
    | ChoiceSet
    | Date
    | Number
    | Text
    | Time
    | Toggle,
    Field(discriminator="type"),
]


for _model in (
    ActionSet,
    ColumnSet,
    Container,
    FactSet,
    Image,
    ImageSet,
    Media,
    RichTextBlock,
    Table,
    TextBlock,
):
    _model.model_rebuild()
