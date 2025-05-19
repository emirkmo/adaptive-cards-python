from typing import Any, TypeVar, Annotated, cast, get_args, Generic, LiteralString
from pydantic.functional_validators import PlainValidator

T = TypeVar("T", bound=LiteralString)


def case_insensitive_literal_validator(
    literal_values: tuple[str, ...],
) -> PlainValidator:
    """
    Returns a PlainValidator that validates a string against a set of allowed literal values (case-insensitive).
    The returned value is always the canonical value from the original tuple.

    Args:
        literal_values (tuple[str, ...]): The allowed literal string values.

    Returns:
        PlainValidator: A Pydantic PlainValidator for use with Annotated.
    """
    mapping: dict[str, str] = {v.lower(): v for v in literal_values}

    def validator(val: Any) -> str:
        """
        Validate that val is a string matching one of the allowed literals (case-insensitive).
        Returns the canonical value from literal_values.
        Raises TypeError if not a string, ValueError if not allowed.
        """
        if not isinstance(val, str):
            raise TypeError("Value must be a string")
        lowered = val.lower()
        if lowered in mapping:
            return mapping[lowered]
        raise ValueError(
            f"Value '{val}' is not a valid literal. Allowed: {literal_values}"
        )

    return PlainValidator(validator)


class CaseInsensitiveLiteralClass(Generic[T]):
    """
    Generic class for case-insensitive literal validation with Pydantic v2.
    Use as CaseInsensitiveLiteral[Literal[...]] to create an Annotated type with a case-insensitive validator.
    """

    def __class_getitem__(cls, literal_type: type[T]) -> type[T]:
        """
        Returns an Annotated type with a case-insensitive validator for the given Literal type.
        Args:
            literal_type (type[T]): A Literal[...] type.
        Returns:
            type[T]: Annotated[Literal, validator]
        Raises:
            TypeError: If not given a Literal type.
        """
        values = get_args(literal_type)
        if not values:
            raise TypeError(
                "CaseInsensitiveLiteral expects a Literal[...] type as input"
            )
        annotated: type[T] = Annotated[
            literal_type, case_insensitive_literal_validator(values)
        ]
        return cast(type[T], annotated)


CaseInsensitiveLiteral = CaseInsensitiveLiteralClass
