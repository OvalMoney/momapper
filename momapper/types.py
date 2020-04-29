__all__ = [
    "ObjectIdType",
    "IntType",
    "FloatType",
    "DecimalType",
    "StringType",
    "ByteType",
    "BoolType",
    "ListType",
    "DictType",
    "ValidationError",
    "Missing",
]

from decimal import Decimal

from bson import Decimal128, ObjectId


class ValidationError(ValueError):
    """Raised when there is an error in the validation of a field value"""

    pass


class Missing(ValidationError):
    """Raised when a required field is missing"""

    pass


class BaseType:
    """Implements validation for field values."""

    def __init__(self, name, value, allow_empty=True):
        """
        :param name: the name of the value to validate.
        :type name: str
        :param value: the value to validate.
        :type value: object
        :param allow_empty: whether the value is allowed to be None or not.
        :type allow_empty: bool
        """
        super().__init__()
        self.name = name
        self.value = value
        self.allow_empty = allow_empty

    def validate(self):
        """The implementation should perform validation of the value."""
        ...

    def marshal(self):
        """The implementation should perform marshalling of the value."""
        ...

    def unmarshal(self):
        """The implementation should perform unmarshalling of the value."""
        ...


class JsonType(BaseType):
    """Implements validation with type checking for JSON fields."""

    typ = None

    def validate(self):
        """Performs validation through type checking on the given value.

        The value should be an instance of ``typ`` to pass validation.
        Otherwise ``ValidationError`` is raised.

        If ``allow_empty`` is False, ``Missing`` is raised when the value is None.
        """
        if self.value is None and self.allow_empty:
            return self.value
        if self.value is None:
            raise Missing(f"{self.name} is required")
        if not type(self.value) == self.typ:
            raise ValidationError(
                f"{self.name} should be {self.typ}. "
                f"Found {self.value}."
            )
        return self.value

    def marshal(self):
        """No marshalling required on a generic JSON value."""
        return self.value

    def unmarshal(self):
        """No unmarshalling required on a generic JSON value."""
        return self.value


class ObjectIdType(JsonType):
    """Performs validation for ObjectId objects."""

    typ = ObjectId


class IntType(JsonType):
    """Performs validation for integer numbers."""

    typ = int


class FloatType(JsonType):
    """Performs validation for floating point numbers."""

    typ = float


class DecimalType(JsonType):
    """Performs validation for Decimal numbers."""

    typ = Decimal

    def marshal(self):
        self.value = Decimal128(self.value)
        return self.value

    def unmarshal(self):
        if isinstance(self.value, Decimal128):
            self.value = self.value.to_decimal()
        elif type(self.value) in (int, float):
            self.value = Decimal(self.value)
        return self.value


class StringType(JsonType):
    """Performs validation for string objects."""

    typ = str


class ByteType(JsonType):
    """Performs validation for bytes objects."""

    typ = bytes


class BoolType(JsonType):
    """Performs validation for boolean objects."""

    typ = bool


class ListType(JsonType):
    """Performs validation for lists."""

    typ = list


class DictType(JsonType):
    """Performs validation for dictionaries."""

    typ = dict
