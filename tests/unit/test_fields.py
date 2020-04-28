from unittest.mock import MagicMock

import pytest

from momapper.fields import NoValue, Field
from momapper.types import Missing


@pytest.fixture
def mocked_field(monkeypatch):
    field = Field("fake", type_=MagicMock())
    monkeypatch.setattr(field, "validator", MagicMock())
    return field


def test_no_value():
    assert bool(NoValue) is False


def test_field_missing_value():
    field = Field("fake", None)
    assert field._missing_value is NoValue
    field = Field("fake", None, if_missing="myvalue")
    assert field._missing_value == "myvalue"
    field = Field("fake", None, if_missing=lambda: "another value")
    assert field._missing_value == "another value"


def test_validator():
    result = object()
    field = Field("fake", type_=MagicMock(return_value=result))
    assert field.validator("value") is result
    field.type_.assert_called_with(value="value", allow_empty=True)


def test_validate(mocked_field):
    result = object()
    mocked_field.validator().marshal.return_value = result
    assert mocked_field.validate("value") is result
    mocked_field.validator.assert_called_with("value")
    mocked_field.validator().unmarshal.assert_called()
    mocked_field.validator().validate.assert_called()
    mocked_field.validator().marshal.assert_called()


def test_validate_missing_default(mocked_field):
    result = object()
    mocked_field.if_missing = "default_value"
    mocked_field.validator().marshal.return_value = result
    mocked_field.validator().unmarshal.side_effect = Missing
    assert mocked_field.validate("value") is result
    mocked_field.validator.assert_called_with("default_value")
    mocked_field.validator().unmarshal.assert_called()
    mocked_field.validator().validate.assert_called()
    mocked_field.validator().marshal.assert_called()


def test_validate_missing_no_default(mocked_field):
    mocked_field.validator().unmarshal.side_effect = Missing
    with pytest.raises(Missing):
        mocked_field.validate("value")
    mocked_field.validator.assert_called_with("value")
    mocked_field.validator().unmarshal.assert_called()
    mocked_field.validator().validate.assert_not_called()
    mocked_field.validator().marshal.assert_not_called()


def test_field_getter(mocked_field):
    result = object()
    document_value = object()
    mocked_field.validator().validate.return_value = result
    mocked_instance = MagicMock()
    mocked_instance._document.get.return_value = document_value

    assert mocked_field.__get__(mocked_instance, "attribute_name") is result

    mocked_instance._document.get.assert_called_with("fake")
    mocked_field.validator.assert_called_with(document_value)
    mocked_field.validator().unmarshal.assert_called()
    mocked_field.validator().validate.assert_called()
    mocked_field.validator().marshal.assert_not_called()


def test_field_setter(mocked_field):
    result = object()
    mocked_field.validator().marshal.return_value = result
    mocked_instance = MagicMock()

    mocked_field.__set__(mocked_instance, "attribute_value")

    mocked_field.validator.assert_called_with("attribute_value")
    mocked_field.validator().unmarshal.assert_not_called()
    mocked_field.validator().validate.assert_called()
    mocked_field.validator().marshal.assert_called()
    mocked_instance._document.__setitem__.assert_called_with("fake", result)
