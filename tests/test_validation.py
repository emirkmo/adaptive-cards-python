from adaptive_cards_python.AdaptiveCard import AdaptiveCard
from pydantic import ValidationError

valid_card = {
    "type": "application/vnd.microsoft.card.adaptive",
    "version": "1.5",
    "body": [
        {
            "type": "TextBlock",
            "text": "Hello, Valid Card!",
            "weight": "bolder",
            "size": "medium"
        }
    ]
}

invalid_card = {
    # missing required 'type' or invalid property
    "version": "1.5",
    "body": []
}


def test_valid_card():
    # This will succeed
    AdaptiveCard.model_validate(valid_card)

def test_invalid_card():
    # This will raise a ValidationError with details from jsonschema
    try:
        AdaptiveCard.model_validate(invalid_card)
    except ValidationError as e:
        print("Schema validation failed:", e)

if __name__ == "__main__":
    #test_invalid_card()
    test_valid_card()