from collections import namedtuple
from unittest.mock import MagicMock

import pytest

from momapper import MappedClass, Field
from momapper.types import StringType, IntType


class Example(MappedClass):
    name = Field("name", StringType)
    count = Field("count", IntType)


@pytest.fixture
def mocked_example(monkeypatch):
    MockedExample = namedtuple("MockedExample", "impl, made_doc, validated")
    with monkeypatch.context() as m:
        made_doc = object()
        m.setattr(Example, "make_document", MagicMock(return_value=made_doc))

        validated = object()
        m.setattr(Example, "validate", MagicMock(return_value=validated))
        yield MockedExample(impl=Example, made_doc=made_doc, validated=validated)


class Cop(MappedClass):
    name = Field("the_name", StringType)
    surname = Field("the_surname", StringType)
    skill_level = Field("skill_level", IntType, required=True, if_missing=0)

