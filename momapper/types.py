__all__ = ['IntType', 'FloatType', 'StringType', 'ByteType',
           'BoolType', 'ListType', 'DictType']

from decimal import Decimal

from bson import Decimal128, ObjectId


class BaseType:
    def __init__(self, value, allow_empty=True):
        super().__init__()
        self.value = value
        self.value = self.validate(self.unmarshal(), allow_empty)

    def validate(self, value, allow_empty=True):
        ...

    def marshal(self):
        ...

    def unmarshal(self):
        ...


class JsonType(BaseType):
    typ = None

    def validate(self, value, allow_empty=True):
        if value is None and allow_empty:
            return value
        if not type(value) == self.typ:
            raise TypeError
        return value

    def marshal(self):
        return self.value

    def unmarshal(self):
        return self.value


class ObjectIdType(JsonType):
    typ = ObjectId


class IntType(JsonType):
    typ = int


class FloatType(JsonType):
    typ = float


class DecimalType(JsonType):
    typ = Decimal

    def marshal(self):
        return Decimal128(self.value)

    def unmarshal(self):
        if isinstance(self.value, Decimal128):
            return self.value.to_decimal()
        return Decimal(self.value)


class StringType(JsonType):
    typ = str


class ByteType(JsonType):
    typ = bytes


class BoolType(JsonType):
    typ = bool


class ListType(JsonType):
    typ = list


class DictType(JsonType):
    typ = dict
