# Adaptive Cards Python

`adaptive_cards_python` is intented to be used as a library for constructing and validating
Microsoft Adaptive Cards within python, without having to refer to any external documentation
or tooling.

## Features

Unlike competing python libraries, it is 100% complete with respect to the official
JSON schema of Adaptive Cards. All possible components are fully implemented, and all descriptions
are also present.

`adaptive_cards_python` supports both programmatic construction of an adaptive card using
type checked components ([Pydantic] models) that allow using your IDE's auto complete
as well as validating existing dict or json string representations of an adaptive card
generated elsewhere.

It is a fully typed, type checked, and run-time validated python implementation of
Microsoft adaptive cards using their (latest as of May 2025) JSON Schema **version 1.5**.
The library has pydantic models that statically type, and run-time validate
adaptive card json/dicts to be compliant with the jsonschema published by [Adaptive Cards].

Each option enum is typed using literal strings, allowing browsing options using your IDE's auto
complete and doc browsing features.

See tests for examples. You can also use the [Interactive Card Designer], but beware of
the barely documented templating syntax. It's only implemented for `C#` and `Javascript`.


[Adaptive Cards]: https://adaptivecards.io/
[Pydantic]: https://docs.pydantic.dev/latest/
[Interactive Card Designer]: https://adaptivecards.io/designer/


## Usage

### Basic validation

```Python
from adaptive_cards_python import AdaptiveCard

# Validate dict
my_python_dict = {"contains json dict representation of adaptive card"}
card = AdaptiveCard.model_validate(my_python_dict)
card.to_dict() # short hand from card.model_dump(exclude_none=True)

# Validate json string
my_python_json_string = '{"contains json dict representation of adaptive card"}'
card = AdaptiveCard.model_validate_json(my_python_json_string)
card.model_dump_json(exclude_none=True)
```

### Construct programmatically

Adaptive cards have a recursive `body` structure made of elements, which can be containers
like `elements.ColumnSet`, individual display components like `elements.TextBlock`,
or user input components like `elements.ChoiceSet`. They also have possible actions
like `actions.OpenUrl`.

```Python
from adaptive_cards python import AdaptiveCard, elements, actions
# Body
body: list[elements.ElementType] = []
body.append(elements.TextBlock(size="medium", weight="bolder", text="TEST TITLE"))

# There are also actions that can be presented to users.
actions_list: list[actions.ActionType] = []
actions_list.append(actions.OpenUrl(title="View url",url="https://some.url"))

card = AdaptiveCard(
        type="AdaptiveCard",
        version="1.5",
        body=body,
        actions=actions_list
    )
```

### Send to msteams

We include a convenience function for sending the adaptive card to msteams via a webhook.
Generate the webhook using the "workflows" app in msteams (you can view your workflows
using [PowerAutomate]).

```Python
from adaptive_cards python import post_to_webhook

MY_WEBHOOK = "<SOME_WEBHOOK>"
# Use previously generated & validated AdaptiveCard as `card`
post_to_webhook(MY_WEBHOOK, card)
```

[PowerAutomate]: https://make.powerautomate.com/

## How It's Made

Pydantic model classes were first generated using `datamodel-code-generator` from the latest (v1.5)
JSON schema of Adaptive Cards. The JSON schema is included in `adaptive_cards/adaptive-card.json`.
Then classes were adapted by hand until circular dependencies were resolved.
We make use of deferred type annotations by using `from __future__ import annotations`,
which allows us to type hint recursive types that reference each other. The models
are then rebuilt at run time using `BaseModel.model_rebuild()` from [Pydantic] to preserve the
type checking capabilities. The included JSON schema is also checked once again for full compliance
using a [Pydantic] `model_validator` and the `jsonschema` package. We use `Literal` in python
to statically type hint and runtime validate accepted enum options. We create a custom base model
`ConfiguredBaseModel` that includes camel case aliasing, and lowercase + whitespace stripped
comparison and validation of included strings.

The only suboptimal trade-off made was for the barely used `ShowCard` action (`actions.ShowCard`).
This action can take in an `AdaptiveCard` and be used inside an `AdaptiveCard`. To keep actions
under their own `actions` namespace, we type hint the card parameter for `ShowCard` using
`dict[str, Any] | ConfiguredBaseModel`. However, we use jsonschema to validate the card inside
of `ShowCard` when constructing the full `AdaptiveCard` anyway.
