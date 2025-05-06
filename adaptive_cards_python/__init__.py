import importlib.metadata

from .adaptive_card import AdaptiveCard, Element as elements, Action as actions
from .validation import validate_using_json_schema
from .msteams import post_to_webhook, create_payload, Payload


try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.0"  # Fallback for development mode

__all__ = [
    "AdaptiveCard",
    "validate_using_json_schema",
    "elements",
    "actions",
    "post_to_webhook",
    "create_payload",
    "Payload",
    "__version__"
]
