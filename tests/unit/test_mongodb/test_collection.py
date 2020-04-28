from unittest.mock import MagicMock

import pytest
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from momapper.mongodb.collection import MappedCollection
from momapper.mongodb.cursor import MappedCursor
from tests.unit.conftest import Cop


@pytest.fixture
def insert_mock(monkeypatch):
    with monkeypatch.context() as m:
        result = InsertOneResult(inserted_id=ObjectId(), acknowledged=True)
        m.setattr(Collection, "insert_one", MagicMock(return_value=result))
        yield result.inserted_id


def test_decorated_collection_insert_one_instance(mongo_client, insert_mock):
    collection = MappedCollection(mongo_client.db, mongo_client.collection, impl=Cop)
    document = {"the_name": "Ray", "the_surname": "Holt", "skill_level": 10}
    obj = Cop()
    obj._document = document
    assert isinstance(collection.insert_one(obj), InsertOneResult)
    assert document["_id"] == insert_mock
    Collection.insert_one.assert_called_with(document)


def test_decorated_collection_insert_one_document(
    monkeypatch, mongo_client, insert_mock
):
    collection = MappedCollection(mongo_client.db, mongo_client.collection, impl=Cop)
    document = {"the_name": "Ray", "the_surname": "Holt", "skill_level": 10}
    monkeypatch.setattr(collection._impl, "validate", MagicMock(return_value=document))
    assert isinstance(collection.insert_one(document), InsertOneResult)
    assert document["_id"] == insert_mock
    Collection.insert_one.assert_called_with(document)
    collection._impl.validate.assert_called_with(document)


def test_decorated_collection_insert_one_skip_validation(
    monkeypatch, mongo_client, insert_mock
):
    collection = MappedCollection(mongo_client.db, mongo_client.collection, impl=Cop)
    document = {"the_name": "Ray", "the_surname": "Holt", "skill_level": 10}
    monkeypatch.setattr(collection._impl, "validate", MagicMock())
    assert isinstance(collection.insert_one(document, _skip_validation=True), InsertOneResult)
    assert document["_id"] == insert_mock
    Collection.insert_one.assert_called_with(document)
    collection._impl.validate.assert_not_called()


def test_decorated_collection_find(mongo_client, monkeypatch):
    collection = MappedCollection(
        mongo_client.db, mongo_client.collection, impl=None
    )
    result = collection.find({"query": "value"})
    assert isinstance(result, MappedCursor)
    assert result.collection is collection
    assert result.__dict__["_Cursor__spec"] == {"query": "value"}


def test_decorated_collection_find_skip_validation(mongo_client, monkeypatch):
    with monkeypatch.context() as m:
        _result = object()
        m.setattr(Collection, "find", MagicMock(return_value=_result))
        collection = MappedCollection(
            mongo_client.db, mongo_client.collection, impl=None
        )
        assert collection.find({"query": "value"}, _skip_validation=True) is _result
        Collection.find.assert_called_with({"query": "value"})
