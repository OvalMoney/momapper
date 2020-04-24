from unittest.mock import MagicMock

from momapper import MongoManager, collection
from momapper.collection import DecoratedCollection


def test_manager_register(mongo_client, monkeypatch):
    with monkeypatch.context() as m:
        _class, _database, _collection = (
            type(object),
            mongo_client.db,
            mongo_client.collection,
        )
        m.setattr(MongoManager, "_registry", {})
        MongoManager.register(_class, _database, _collection)
        registered = MongoManager._registry[_class]
        assert isinstance(registered, DecoratedCollection)
        assert registered.name == _collection
        assert registered._impl is _class
        assert registered.database is _database


def test_manager_get_collection(monkeypatch):
    with monkeypatch.context() as m:
        _class = type(object)
        m.setattr(MongoManager, "_registry", MagicMock())
        MongoManager.get_collection(_class)
        MongoManager._registry.__getitem__.assert_called_with(_class)


def test_collection_function(monkeypatch):
    with monkeypatch.context() as m:
        _class, _result = type(object), object()
        m.setattr(MongoManager, "get_collection", MagicMock(return_value=_result))
        assert collection(_class) is _result
        MongoManager.get_collection.assert_called_with(_class)
