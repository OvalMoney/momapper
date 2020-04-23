from decimal import Decimal

from bson import Decimal128


class NoValueType:
    def __bool__(self):
        return False


NoValue = NoValueType()  # marker


class Field:
    def __init__(self, field, type_, if_missing=NoValue, required=False):
        self.field = field
        self.type_ = type_
        self.if_missing = if_missing
        self.required = required

    @staticmethod
    def encode_to_mongo(value):
        if isinstance(value, Decimal):
            return Decimal128(value)
        return value

    @staticmethod
    def decode_from_mongo(value):
        if isinstance(value, Decimal128):
            return value.to_decimal()
        return value

    def extract(self, document):
        value = Field.decode_from_mongo(document.get(self.field, NoValue))
        if value is NoValue:
            if not self.required:
                document[self.field] = (
                    self.if_missing() if callable(self.if_missing) else self.if_missing
                )
                return document[self.field]
            raise ValueError(f"missing value {self.field}")
        return value

    def validate(self, value):
        if value in (None, NoValue):
            if self.required:
                raise ValueError(
                    f"{self.field} is required. " f"Found {value}({type(value)}"
                )
            return None
        if not isinstance(value, self.type_):
            raise ValueError(
                f"value {value}({type(value)}) for "
                f"field {self.field} is not {self.type_}"
            )

        return value

    def __get__(self, instance, owner):
        if instance is None:
            return self

        not_validated_value = self.extract(instance._document)
        validated = self.validate(not_validated_value)
        return validated

    def __set__(self, instance, value):
        validated = self.validate(value)
        instance._document[self.field] = validated
