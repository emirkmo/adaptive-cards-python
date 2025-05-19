from __future__ import annotations
from pydantic import BaseModel, ValidationError
from typing import Literal, Annotated
from adaptive_cards_python.case_insensitive_literal import CaseInsensitiveLiteral
import pytest

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
    with pytest.raises(AssertionError):
        assert getattr(ann, "__origin__", None).__name__ == "Annotated"
    assert getattr(ann, "__origin__", None).__name__ == "Literal"
    assert set(ann.__args__) == {"Some", "Config"}
