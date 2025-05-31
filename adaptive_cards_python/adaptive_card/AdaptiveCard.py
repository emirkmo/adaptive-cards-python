from __future__ import annotations  # Required to defer type hint evaluation!

from typing import Any, Literal, Self
from pathlib import Path
import json

from pydantic import AnyUrl, Field, model_validator
import jsonschema

from .config import VerticalContentAlignment
from .Action import Execute, ISelectActionType, ActionType
from .BackgroundImage import BackgroundImage
from .Element import ElementType
from .Extendable import ConfiguredBaseModel


def get_json_schema_json() -> dict[str, Any]:
    """Return the adaptive-card.json json schema as a python dict using json.load"""
    adaptive_card_json_schema_path = Path(__file__).parent / "adaptive-card.json"
    with adaptive_card_json_schema_path.open() as outfile:
        return json.load(outfile)


class AuthCardButton(ConfiguredBaseModel):
    """
    Defines a button as displayed when prompting a user to authenticate.
    This maps to the cardAction type defined by the Bot Framework
    (https://docs.microsoft.com/dotnet/api/microsoft.bot.schema.cardaction).
    """

    type: str = Field(..., description="The type of the button.")
    title: str | None = Field(default=None, description="The caption of the button.")
    image: str | None = Field(
        default=None,
        description="A URL to an image to display alongside the button's caption.",
    )
    value: str = Field(
        ...,
        description=(
            "The value associated with the button. The meaning of value depends on the"
            " button's type."
        ),
    )


class TokenExchangeResource(ConfiguredBaseModel):
    """
    Defines information required to enable on-behalf-of single sign-on user authentication.
    Maps to the TokenExchangeResource type defined by the Bot Framework
    (https://docs.microsoft.com/dotnet/api/microsoft.bot.schema.tokenexchangeresource)
    """

    type: Literal["TokenExchangeResource"] = Field(
        default="TokenExchangeResource", description="Must be `TokenExchangeResource`"
    )
    id: str = Field(
        ..., description="The unique identified of this token exchange instance."
    )
    uri: str = Field(
        ...,
        description=(
            "An application ID or resource identifier with which to exchange a token on"
            " behalf of. This property is identity provider- and application-specific."
        ),
    )
    providerId: str = Field(
        ...,
        description=(
            "An identifier for the identity provider with which to attempt a token"
            " exchange."
        ),
    )


class Authentication(ConfiguredBaseModel):
    """
    Defines authentication information associated with a card.
    This maps to the OAuthCard type defined by the Bot Framework
    (https://docs.microsoft.com/dotnet/api/microsoft.bot.schema.oauthcard)
    """

    type: Literal["Authentication"] = Field(
        default="Authentication",
        description="Must be `Authentication`",
    )
    text: str | None = Field(
        default=None,
        description=(
            "Text that can be displayed to the end user when prompting them to"
            " authenticate."
        ),
    )
    connectionName: str | None = Field(
        default=None,
        description=(
            "The identifier for registered OAuth connection setting information."
        ),
    )
    tokenExchangeResource: TokenExchangeResource | None = Field(
        default=None,
        description=(
            "Provides information required to enable on-behalf-of single sign-on user"
            " authentication."
        ),
    )
    buttons: list[AuthCardButton] | None = Field(
        default=None,
        description=(
            "Buttons that should be displayed to the user when prompting for"
            ' authentication. The array MUST contain one button of type "signin". Other'
            " button types are not currently supported."
        ),
    )


class AdaptiveCard(ConfiguredBaseModel):
    """
    An Adaptive Card, containing a free-form body of card elements, and an optional set of actions.
    """

    type: Literal["AdaptiveCard", "application/vnd.microsoft.card.adaptive"] = Field(
        "AdaptiveCard",
        description="Must be `AdaptiveCard`",
    )
    version: str = Field(
        default="1.5",
        description=(
            "Schema version that this card requires. If a client is **lower** than this"
            " version, the `fallbackText` will be rendered. NOTE: Version is not"
            " required for cards within an `Action.ShowCard`. However, it *is* required"
            " for the top-level card."
        ),
        examples=["1.0", "1.1", "1.2"],
    )
    refresh: Refresh | None = Field(
        default=None,
        description=(
            "Defines how the card can be refreshed by making a request to the target"
            " Bot."
        ),
        json_schema_extra={"version": "1.4"},
    )
    authentication: Authentication | None = Field(
        default=None,
        description=(
            "Defines authentication information to enable on-behalf-of single sign on"
            " or just-in-time OAuth."
        ),
        json_schema_extra={"version": "1.4"},
    )
    body: list[ElementType] | None = Field(
        default=None,
        description="The card elements to show in the primary card region.",
    )
    actions: list[ActionType] | None = Field(
        default=None, description="The Actions to show in the card's action bar."
    )
    selectAction: ISelectActionType | None = Field(
        default=None,
        description=(
            "An Action that will be invoked when the card is tapped or selected."
            " `Action.ShowCard` is not supported."
        ),
        json_schema_extra={"version": "1.1"},
    )
    fallbackText: str | None = Field(
        default=None,
        description=(
            "Text shown when the client doesn't support the version specified (may"
            " contain markdown)."
        ),
    )
    backgroundImage: BackgroundImage | str | None = Field(
        default=None,
        description="Specifies the background image of the card.",
        json_schema_extra={"version": "1.2"},
    )
    minHeight: str | None = Field(
        default=None,
        description="Specifies the minimum height of the card.",
        examples=["50px"],
        json_schema_extra={"version": "1.2", "features": [2293]},
    )
    rtl: bool | None = Field(
        default=None,
        description=(
            "When `true` content in this Adaptive Card should be presented right to"
            " left. When 'false' content in this Adaptive Card should be presented left"
            " to right. If unset, the default platform behavior will apply."
        ),
        json_schema_extra={"version": "1.5"},
    )
    speak: str | None = Field(
        default=None,
        description=(
            "Specifies what should be spoken for this entire card. This is simple text"
            " or SSML fragment."
        ),
    )
    lang: str | None = Field(
        default=None,
        description=(
            "The 2-letter ISO-639-1 language used in the card. Used to localize any"
            " date/time functions."
        ),
        examples=["en", "fr", "es"],
    )
    verticalContentAlignment: VerticalContentAlignment | None = Field(
        default=None,
        description=(
            "Defines how the content should be aligned vertically within the container."
            " Only relevant for fixed-height cards, or cards with a `minHeight`"
            " specified."
        ),
        json_schema_extra={"version": "1.1"},
    )
    field_schema: AnyUrl | None = Field(
        default=None, alias="$schema", description="The Adaptive Card schema."
    )

    @model_validator(mode="after")
    def validate_using_json_schema(self: Self) -> Self:
        schema_json = get_json_schema_json()
        self.type = "AdaptiveCard"  # Do we need this?

        jsonschema.validate(
            instance=self.model_dump(exclude_none=True), schema=schema_json
        )
        return self

    def to_dict(self) -> dict[str, Any]:
        """Dump correctly using model_dump(exclude_none=True)"""
        return self.model_dump(exclude_none=True)

    def to_json(self) -> str:
        """Dump correctly using model_dump_json(exclude_none=True)"""
        return self.model_dump_json(exclude_none=True)


class Refresh(ConfiguredBaseModel):
    """
    Defines how a card can be refreshed by making a request to the target Bot.
    """

    type: Literal["Refresh"] = Field(default="Refresh", description="Must be `Refresh`")
    action: Execute | None = Field(
        default=None,
        description=(
            "The action to be executed to refresh the card. Clients can run this"
            " refresh action automatically or can provide an affordance for users to"
            " trigger it manually."
        ),
    )
    userIds: list[str] | None = Field(
        default=None,
        description=(
            "A list of user Ids informing the client for which users should the refresh"
            " action should be run automatically. Some clients will not run the refresh"
            " action automatically unless this property is specified. Some clients may"
            " ignore this property and always run the refresh action automatically."
        ),
    )


AdaptiveCard.model_rebuild()
