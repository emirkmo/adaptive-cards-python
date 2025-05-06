from __future__ import annotations  # Required to defer type hint evaluation!

from typing import Annotated, Any, Literal
from pathlib import Path
from pydantic import Field, ConfigDict

from .Extendable import Item, ConfiguredBaseModel
from .config import FallbackOption

import orjson


ActionMode = Literal["primary", "secondary"]

ActionStyle = Literal["default", "positive", "destructive"]


class ActionBase(Item):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    title: str | None = Field(
        default=None,
        description="Label for button or link that represents this action.",
    )
    iconUrl: str | None = Field(
        default=None,
        description=(
            "Optional icon to be shown on the action in conjunction with the title."
            " Supports data URI in version 1.2+"
        ),
        json_schema_extra={"version": "1.1"},
    )
    id: str | None = Field(
        default=None, description="A unique identifier associated with this Action."
    )
    style: ActionStyle | None = Field(
        default=None,
        description=(
            "Controls the style of an Action, which influences how the action is"
            " displayed, spoken, etc."
        ),
        json_schema_extra={"version": "1.2"},
    )
    fallback: "ActionType | FallbackOption | None" = Field(
        default=None,
        description=(
            "Describes what to do when an unknown element is encountered or the"
            " requires of this or any children can't be met."
        ),
        json_schema_extra={"version": "1.2"},
    )
    tooltip: str | None = Field(
        default=None,
        description=(
            "Defines text that should be displayed to the end user as they hover the"
            " mouse over the action, and read when using narration software."
        ),
        json_schema_extra={"version": "1.5"},
    )
    isEnabled: bool | None = Field(
        default=True,
        description="Determines whether the action should be enabled.",
        json_schema_extra={"version": "1.5"},
    )
    mode: ActionMode = Field(
        default="primary",
        description=(
            "Determines whether the action should be displayed as a button or in the"
            " overflow menu."
        ),
        json_schema_extra={"version": "1.5"},
    )


AssociatedInputs = Literal["Auto", "None"]


def get_json_schema_file() -> Path:
    json_schema_file = Path(__file__).parent / "adaptive-card.json"
    assert json_schema_file.is_file
    return json_schema_file


class TargetElement(ConfiguredBaseModel):
    """
    Represents an entry for Action.ToggleVisibility's targetElements property
    """

    type: Literal["TargetElement"] = Field(
        default="TargetElement", description="Must be `TargetElement`"
    )
    elementId: str = Field(..., description="Element ID of element to toggle")
    isVisible: bool | None = Field(
        default=None,
        description=(
            "If `true`, always show target element. If `false`, always hide target"
            " element. If not supplied, toggle target element's visibility. "
        ),
    )


class Execute(ActionBase):
    """
    Gathers input fields, merges with optional data field, and sends an event to the client.
    Clients process the event by sending an Invoke activity of type adaptiveCard/action
    to the target Bot. The inputs that are gathered are those on the current card, and in
    the case of a show card those on any parent cards. See [Universal Action Model]
    (https://docs.microsoft.com/en-us/adaptive-cards/authoring-cards/universal-action-model)
    documentation for more details.
    """

    type: Literal["Action.Execute"] = Field(
        default="Action.Execute", description="Must be `Action.Execute`"
    )
    verb: str | None = Field(
        default=None,
        description="The card author-defined verb associated with this action.",
    )
    data: str | dict[str, Any] | None = Field(
        default=None,
        description=(
            "Initial data that input fields will be combined with. These are"
            " essentially ‘hidden’ properties."
        ),
    )
    associatedInputs: AssociatedInputs = Field(
        default="Auto",
        description="Controls which inputs are associated with the action.",
    )


class OpenUrl(ActionBase):
    """
    When invoked, show the given url either by launching it in an external web browser or
    showing within an embedded web browser.
    """

    type: Literal["Action.OpenUrl"] = Field(
        default="Action.OpenUrl", description="Must be `Action.OpenUrl`"
    )
    url: str = Field(..., description="The URL to open.")


class ShowCard(ActionBase):
    """
    Defines an AdaptiveCard which is shown to the user when the button or link is clicked.
    """

    type: Literal["Action.ShowCard"] = Field(
        default="Action.ShowCard", description="Must be `Action.ShowCard`"
    )
    card: dict[str, Any] | ConfiguredBaseModel = Field(
        ...,
        description=(
            "The Adaptive Card to show. Inputs in ShowCards will not be submitted if"
            " the submit button is located on a parent card. See"
            " https://docs.microsoft.com/en-us/adaptive-cards/authoring-cards/input-validation"
            " for more details. **WARNING:** Type hinting is suboptimal but input is validated"
        ),
        json_schema_extra=orjson.loads(get_json_schema_file().read_bytes()),
    )


class Submit(ActionBase):
    """
    Gathers input fields, merges with optional data field, and sends an event to the client.
    It is up to the client to determine how this data is processed. For example: With BotFramework bots,
    the client would send an activity through the messaging medium to the bot.
    The inputs that are gathered are those on the current card,
    and in the case of a show card those on any parent cards.
    See https://docs.microsoft.com/en-us/adaptive-cards/authoring-cards/input-validation
    for more details.
    """

    type: Literal["Action.Submit"] = Field(
        default="Action.Submit", description="Must be `Action.Submit`"
    )
    data: str | dict[str, Any] | None = Field(
        default=None,
        description=(
            "Initial data that input fields will be combined with. These are"
            " essentially ‘hidden’ properties."
        ),
    )
    associatedInputs: AssociatedInputs | None = Field(
        "Auto",
        description="Controls which inputs are associated with the submit action.",
        json_schema_extra={"version": "1.3"},
    )


class ToggleVisibility(ActionBase):
    """
    An action that toggles the visibility of associated card elements.
    """

    type: Literal["Action.ToggleVisibility"] = Field(
        default="Action.ToggleVisibility",
        description="Must be `Action.ToggleVisibility`",
    )
    targetElements: list[TargetElement | str] = Field(
        ...,
        description=(
            "The array of TargetElements. It is not recommended to include Input"
            " elements with validation under Action.Toggle due to confusion that can"
            " arise from invalid inputs that are not currently visible. See"
            " https://docs.microsoft.com/en-us/adaptive-cards/authoring-cards/input-validation"
            " for more information."
        ),
    )


ActionType = Annotated[
    Execute | OpenUrl | ShowCard | Submit | ToggleVisibility,
    Field(discriminator="type"),
]

ISelectActionType = Annotated[
    Execute | OpenUrl | Submit | ToggleVisibility, Field(discriminator="type")
]

for _model in (Execute, OpenUrl, ShowCard, Submit, ToggleVisibility):
    _model.model_rebuild()
