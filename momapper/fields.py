from momapper.types import Missing


class NoValueType:
    """Marker that signals a missing value != None."""

    def __bool__(self):
        return False


NoValue = NoValueType()  # marker


class Field:
    """Field class to use for schema declaration.

    All the attributes of a :py:class:`MappedClass` that are instances of
    :py:class:`Field` are used for schema validation.
    """

    def __init__(self, field, type_, if_missing=NoValue, required=False):
        """
        :param field: The field name.
        :type field: str
        :param type_: The field type.
        :type type_: BaseType
        :param if_missing: value to use, or function to call if the value is not found in the document.
        If set to ``NoValue`` it won't be considered. Defaults to ``NoValue``.
        :type if_missing: object
        :param required: whether the field is required in the schema.
        :type required: bool
        """
        self.field = field
        self.type_ = type_
        self.if_missing = if_missing
        self.required = required

    @property
    def _missing_value(self):
        """Return the missing value by calling ``if_missing`` if necessary."""
        return self.if_missing() if callable(self.if_missing) else self.if_missing

    def validator(self, value):
        """Return the ``BaseType`` instance to perform validation.

        :param value: the value to perform validation onto.
        :type value: object.
        :return: the field validator.
        :rtype: BaseType
        """
        return self.type_(value=value, allow_empty=not self.required)

    def validate(self, value):
        """Executes validation of the given value.

        Validation is performed by running the complete pipeline of validation
        on the ``BaseType`` instance:
            1. ``BaseType.unmarshal()`` to unmarshal a value that possibly comes from raw data.
            2. ``BaseType.validate()`` to validate the unmarshalled value.
            3. ``BaseType.marshal()`` to marshal the value again in the right format.
        The validated value is then returned.

        If the value is not found and it was required, the return value of ``if_missing``
        is returned instead, but only if it was given.
        The value returned from ``if_missing`` undergoes validation itself too,
        but 1. is not applied, assuming that the developer implements ``if_missing``
        to return an already unmarshalled value.

        :param value: the value to validate.
        :type value: object
        :return: the value after validation.
        :rtype: object
        """
        try:
            validator = self.validator(value)
            validator.unmarshal()
            validator.validate()
            return validator.marshal()
        except Missing:
            if self.if_missing is NoValue:
                raise
            validator = self.validator(self._missing_value)
            validator.validate()
            return validator.marshal()

    def __get__(self, instance, owner):
        """Override getter of field to validate outgoing values.

        The value of the field is taken from the ``_document`` property
        of the ``MappedClass`` instance, and validated after performing
        unmarshalling.
        """
        if instance is None:
            return self

        not_validated_value = instance._document.get(self.field)
        validator = self.validator(not_validated_value)
        validator.unmarshal()
        return validator.validate()

    def __set__(self, instance, value):
        """Override getter of field to validate ingoing values.

        The value of the field is set onto the ``_document`` property
        of the ``MappedClass`` instance, validated and marshalled.
        """
        validator = self.validator(value)
        validator.validate()
        instance._document[self.field] = validator.marshal()
