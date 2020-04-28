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

    @property
    def _missing_value(self):
        return self.if_missing() if callable(self.if_missing) else self.if_missing

    def validator(self, value):
        return self.type_(value=value, allow_empty=not self.required)

    def validate(self, value):
        if value in (None, NoValue):
            if self.required:
                if self.if_missing is not NoValue:
                    return self._missing_value
                raise ValueError(
                    f"{self.field} is required. Found {value}({type(value)}"
                )
            return None

        return self.validator(value).marshal()

    def __get__(self, instance, owner):
        if instance is None:
            return self

        not_validated_value = instance._document.get(self.field, NoValue)
        validated = self.validator(not_validated_value).value
        return validated

    def __set__(self, instance, value):
        validated = self.validator(value).marshal()
        instance._document[self.field] = validated
