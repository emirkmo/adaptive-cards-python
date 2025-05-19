from typing import Any, TypeVar, Annotated, cast, get_args, Generic, LiteralString
from pydantic.functional_validators import PlainValidator

T = TypeVar("T", bound=LiteralString)

def case_insensitive_literal_validator(literal_values: tuple[str, ...]) -> Any:
    mapping = {v.lower(): v for v in literal_values}
    def validator(val: Any) -> str:
        if not isinstance(val, str):
            raise TypeError("Value must be a string")
        lowered = val.lower()
        if lowered in mapping:
            return mapping[lowered]
        raise ValueError(f"Value '{val}' is not a valid literal. Allowed: {literal_values}")
    return PlainValidator(validator)

class CaseInsensitiveLiteralClass(Generic[T]):
    def __class_getitem__(cls, literal_type: type[T]) -> type[T]:
        values = get_args(literal_type)
        if not values:
            raise TypeError("CaseInsensitiveLiteral expects a Literal[...] type as input")
        annotated = Annotated[literal_type, case_insensitive_literal_validator(values)]
        return cast(type[T], annotated)

CaseInsensitiveLiteral = CaseInsensitiveLiteralClass
