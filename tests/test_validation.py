import datetime
from adaptive_cards_python import (
    AdaptiveCard,
    validate_using_json_schema,
    elements,
    actions,
)
from pydantic import ValidationError
import requests
import pytest

valid_card = {
    "type": "AdaptiveCard",
    "version": "1.5",
    "body": [
        {
            "type": "TextBlock",
            "text": "Hello, Valid Card!",
            "weight": "bolder",
            "size": "medium",
        }
    ],
}

invalid_card = {
    # missing required 'type' or invalid property
    "version": "1.5",
    "body": [],
}
WEBHOOK_URL = "<MY_MSTEAMS_WORKFLOW_WEBHOOK_URL>"


def test_valid_card():
    # This will succeed
    card_model = AdaptiveCard.model_validate(valid_card)

    # This should also succeed
    validate_using_json_schema(card_model.model_dump(exclude_unset=True))


def test_invalid_card():
    # This will raise a ValidationError with details from jsonschema
    try:
        AdaptiveCard.model_validate(invalid_card)
    except ValidationError as e:
        print("Schema validation failed:", e)


@pytest.mark.skip
def test_send_adaptive_card():
    card_model = AdaptiveCard.model_validate(valid_card)
    payload = {
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card_model.model_dump(exclude_unset=True),
            }
        ]
    }

    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    assert resp.text == ""


def test_construct_card():
    body: list[elements.ElementType] = []

    body.append(elements.TextBlock(size="medium", weight="bolder", text="TEST TITLE"))

    body.append(
        elements.ColumnSet(
            columns=[
                elements.Column(
                    items=[
                        elements.Image(
                            style="person",
                            url="https://www.axis.com/themes/custom/axiscom/logo.png",
                            altText="Axis logo",
                            size="small",
                        )
                    ],
                    width="auto",
                ),
                elements.Column(
                    items=[
                        elements.TextBlock(
                            weight="bolder", wrap=True, text="DDM Dagster Bot"
                        ),
                        elements.TextBlock(
                            spacing=None,
                            isSubtle=True,
                            wrap=True,
                            text=f"Created {datetime.datetime.now().isoformat()}",
                        ),
                    ],
                    width="stretch",
                ),
            ],
        )
    )
    body.append(elements.TextBlock(text="Test alert text block", wrap=True))
    body.append(
        elements.FactSet(
            facts=[
                elements.Fact(title="fact0_key", value="fact0_value"),
                elements.Fact(title="fact1_key", value="fact1_value"),
            ]
        )
    )

    actions_list: list[actions.ActionType] = []
    actions_list.append(
        actions.OpenUrl(
            title="View Contract",
            url="https://github.com/axteams-one/ddm-contracts/blob/main/contracts/idd/acap_list.yaml",
        )
    )

    AdaptiveCard(type="AdaptiveCard", version="1.5", body=body, actions=actions_list)


def contruct_from_dict():
    AdaptiveCard.model_validate(
        {
            "type": "AdaptiveCard",
            "version": "1.5",
            "refresh": {
                "action": {
                    "type": "Action.Execute",
                    "title": "Refresh Card",
                    "verb": "refreshCard",
                },
            },
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Here is an existing card that you can reply to or update:",
                    "wrap": "true",
                },
                {
                    "type": "Input.Text",
                    "id": "userResponse",
                    "placeholder": "Type your reply or updated text here...",
                },
            ],
            "actions": [
                {
                    "type": "Action.Execute",
                    "title": "Update Card",
                    "verb": "updateCard",
                    "data": {"newText": "${userResponse}"},
                },
            ],
        }
    )


def test_construct_from_json_string():
    card_json = """{
            "type": "AdaptiveCard",
            "version": "1.5",
            "refresh": {
                "action": {
                    "type": "Action.Execute",
                    "title": "Refresh",
                    "verb": "acceptRejectView"
                }
            },
            "body": [
                {"type": "TextBlock", "text": "Migrations Ready"},
                {"type": "TextBlock", "text": "Submitted by **ADACO**"},
                {
                    "type": "TextBlock",
                    "text": "Approval pending from **DDM**"
                }
            ],
            "actions": [
                {
                    "type": "Action.Execute",
                    "title": "Approve",
                    "verb": "approve",
                    "data": {"more info": "<more info>"}
                },
                {
                    "type": "Action.Execute",
                    "title": "Reject",
                    "verb": "reject",
                    "data": {"more info": "<more info>"}
                }
            ]
        }
    """
    AdaptiveCard.model_validate_json(card_json)
