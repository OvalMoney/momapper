import pytest

from momapper import Field
from momapper.mappedclass import ValidatorMeta
from momapper.types import StringType, IntType
from tests.unit.conftest import Cop


def test_validator_meta_no_fields():
    class NoFields(metaclass=ValidatorMeta):
        pass

    assert NoFields.__fields__ == {}


def test_validator_meta_fields_no_name():
    class NoNameFields(metaclass=ValidatorMeta):
        name = Field(None, StringType)
        count = Field(None, IntType)

    assert NoNameFields.__fields__ == {"name": "name", "count": "count"}


def test_validator_meta_fields_with_name():
    class NameFields(metaclass=ValidatorMeta):
        name = Field("name_field", StringType)
        count = Field("count_field", StringType)

    assert NameFields.__fields__ == {"name": "name_field", "count": "count_field"}


def test_mappedclass_init_kwargs(mocked_example):
    kwargs = {"name": "Jake", "count": 10}
    example_obj = mocked_example.impl(**kwargs)
    mocked_example.impl.make_document.assert_called_with(**kwargs)
    mocked_example.impl.validate.assert_called_with(mocked_example.made_doc)
    assert example_obj._document is mocked_example.validated


def test_mappedclass_init_document(mocked_example):
    document = {"name": "Peralta", "count": 10}
    example_obj = mocked_example.impl(_document=document)
    mocked_example.impl.make_document.assert_not_called()
    mocked_example.impl.validate.assert_called_with(document)
    assert example_obj._document is mocked_example.validated


@pytest.mark.parametrize(
    "kwargs, document",
    [
        (
            {"name": "Terry", "surname": "Crews", "skill_level": 7},
            {"the_name": "Terry", "the_surname": "Crews", "skill_level": 7},
        ),
        (
            {"name": "Jake", "surname": "Peralta"},
            {"the_name": "Jake", "the_surname": "Peralta"},
        ),
    ],
)
def test_mappedclass_make_document(kwargs, document):
    assert Cop.make_document(**kwargs) == document


def test_mappedclass_invalid_field():
    with pytest.raises(KeyError):
        Cop.make_document(invalid="key", name="Seth", surname="Dozerman")


@pytest.mark.parametrize(
    "document, validated",
    [
        (
            {"the_name": "Terry", "the_surname": "Crews", "skill_level": 7},
            {"the_name": "Terry", "the_surname": "Crews", "skill_level": 7},
        ),
        (
            {"the_name": "Jake", "the_surname": "Peralta"},
            {"the_name": "Jake", "the_surname": "Peralta", "skill_level": 0},
        ),
    ],
)
def test_mappedclass_validate(document, validated):
    assert Cop.validate(document) == validated


def test_mappedclass_validate_invalid():
    with pytest.raises(TypeError):
        Cop.validate(
            {"the_name": "Jake", "the_surname": "Peralta", "skill_level": "genius"}
        )
