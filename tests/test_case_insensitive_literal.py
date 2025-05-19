from __future__ import annotations
from pydantic import BaseModel, ValidationError, TypeAdapter
from pydantic.functional_validators import PlainValidator
from typing import Literal, Union
import pytest
from adaptive_cards_python.case_insensitive_literal import (
    CaseInsensitiveLiteral,
    case_insensitive_literal_validator,
)

SomeConfig = Literal["Some", "Config"]


class TestClass(BaseModel):
    test: CaseInsensitiveLiteral[SomeConfig]


def test_accepts_any_case():
    for val in ["Some", "some", "SOME", "sOmE"]:
        assert TestClass(test=val).test == "Some"
    for val in ["Config", "config", "CONFIG", "cOnFiG"]:
        assert TestClass(test=val).test == "Config"
    with pytest.raises(ValidationError):
        TestClass(test="other")


def test_literal_type():
    ann = TestClass.model_fields["test"].annotation
    # At runtime, Pydantic exposes the base Literal, not Annotated
    assert getattr(ann, "__origin__", None).__name__ == "Literal"
    assert set(ann.__args__) == {"Some", "Config"}


def test_case_insensitive_literal_as_is():
    """Test CaseInsensitiveLiteral with various input cases."""

    class Model1(BaseModel):
        value: CaseInsensitiveLiteral[Literal["Case"]]

    for val in ["Case", "case", "CASE", "CaSe"]:
        assert Model1(value=val).value == "Case"

    # Test a mapping that should all be equivalent
    class Model2(BaseModel):
        value: CaseInsensitiveLiteral[Literal["Case", "CASe", "case"]]

    # Document the limitation: the canonical value is always the last occurrence
    assert Model2(value="Case").value == "case"
    assert Model2(value="CASe").value == "case"
    assert Model2(value="case").value == "case"
    assert Model2(value="cAse").value == "case"
    assert Model2(value="CASE").value == "case"

    # Multiworded case-insensitive literal
    class Model3(BaseModel):
        value: CaseInsensitiveLiteral[Literal["caseCase"]]

    for val in ["caseCase", "CASECASE", "CaseCase", "casecase"]:
        assert Model3(value=val).value == "caseCase"

    class Model4(BaseModel):
        value: CaseInsensitiveLiteral[
            Literal["caseCase", "CASECASE", "Casecase", "CASEcase"]
        ]

    assert Model4(value="caseCase").value == "CASEcase"
    assert Model4(value="CASECASE").value == "CASEcase"
    assert Model4(value="Casecase").value == "CASEcase"
    assert Model4(value="CASEcase").value == "CASEcase"
    assert Model4(value="casecase").value == "CASEcase"
    assert Model4(value="CaSeCaSe").value == "CASEcase"


# 2. Used in a nested model


class TestNestedModelValue(BaseModel):
    value: CaseInsensitiveLiteral[Literal["Nested", "NESTED", "nested"]]


class NestedModel(BaseModel):
    nested: TestNestedModelValue
    value: CaseInsensitiveLiteral[Literal["Nested", "NESTED", "nested"]]


def test_case_insensitive_literal_in_nested_model():
    """Test use of CaseInsensitiveLiteral in a Nested Pydantic Model, including roundtripping."""
    # Direct instantiation
    model = NestedModel(value="Nested", nested={"value": "NESTED"})
    assert model.value == "nested"
    assert model.nested.value == "nested"

    # Roundtrip: model -> dict -> model_validate
    data = model.model_dump()
    model2 = NestedModel.model_validate(data)
    assert model2.value == "nested"
    assert model2.nested.value == "nested"

    # Roundtrip: model -> json -> model_validate_json
    json_str = model.model_dump_json()
    model3 = NestedModel.model_validate_json(json_str)
    assert model3.value == "nested"
    assert model3.nested.value == "nested"

    # All other case-insensitive matches will map to the last occurrence
    assert NestedModel(value="NeStEd", nested={"value": "nEsTeD"}).value == "nested"
    assert (
        NestedModel(value="NeStEd", nested={"value": "nEsTeD"}).nested.value == "nested"
    )

    # Document the limitation: the canonical value is always the last occurrence
    with pytest.raises(ValidationError):
        NestedModel(value="notnested", nested={"value": "nested"})
    with pytest.raises(ValidationError):
        NestedModel(value="nested", nested={"value": "notnested"})


def test_case_insensitive_literal_validator():
    """Test the validator function via a Pydantic model and also directly."""

    # Directly using the validator function
    validator_obj = case_insensitive_literal_validator(("foo", "bar"))

    assert isinstance(validator_obj, PlainValidator)
    # Access the inner function for direct testing
    inner_validator = validator_obj.func
    # Accepts any case, returns canonical value
    assert inner_validator("FOO") == "foo"
    assert inner_validator("foo") == "foo"
    assert inner_validator("FoO") == "foo"
    assert inner_validator("BAR") == "bar"
    assert inner_validator("bar") == "bar"
    assert inner_validator("bAr") == "bar"
    # Invalid value raises ValueError
    with pytest.raises(ValueError):
        inner_validator("baz")
    with pytest.raises(TypeError):
        inner_validator(123)

    # Also test via a Pydantic model
    class Model(BaseModel):
        value: CaseInsensitiveLiteral[Literal["foo", "bar"]]

    assert Model(value="FOO").value == "foo"
    assert Model(value="Bar").value == "bar"
    with pytest.raises(ValidationError):
        Model(value="baz")


# 4. Known failure: use as a discriminator in a tagged union
class A(BaseModel):
    type: CaseInsensitiveLiteral[Literal["A"]]
    value: int


class B(BaseModel):
    type: CaseInsensitiveLiteral[Literal["B"]]
    value: int


class ALit(BaseModel):
    type: Literal["A"]
    value: int


class BLit(BaseModel):
    type: Literal["B"]
    value: int


TaggedUnion = TypeAdapter(Union[ALit, BLit])


@pytest.mark.xfail(
    reason="CaseInsensitiveLiteral cannot be used as a discriminator in Pydantic V2"
)
def test_case_insensitive_literal_discriminator_fails():
    with pytest.raises(Exception):
        TypeAdapter(Union[A, B])


# 5. Literal-based union works
@pytest.mark.parametrize(
    "data,expected",
    [
        ({"type": "A", "value": 1}, ALit),
        ({"type": "B", "value": 2}, BLit),
    ],
)
def test_literal_discriminator_works(data, expected):
    obj = TaggedUnion.validate_python(data)
    assert isinstance(obj, expected)
