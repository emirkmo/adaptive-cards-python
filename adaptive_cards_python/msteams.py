from typing import Any, Literal, TypedDict
import requests

from .adaptive_card import AdaptiveCard


class Attachment(TypedDict):
    contentType: Literal["application/vnd.microsoft.card.adaptive"]
    content: dict[str, Any]


class Payload(TypedDict):
    attachments: list[Attachment]


def create_payload(adaptive_card: AdaptiveCard) -> Payload:
    """Get msteams payload for post request"""
    payload: Payload = {
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": adaptive_card.to_dict(),
            }
        ]
    }
    return payload


def post_to_webhook(webhook_url: str, card: AdaptiveCard) -> requests.Response:
    """Post as payload to msteams webhook. Create via power automate."""
    resp = requests.post(webhook_url, json=create_payload(card))
    resp.raise_for_status()
    assert resp.text == ""
    return resp
