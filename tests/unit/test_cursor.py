from unittest.mock import MagicMock

import pytest
from pymongo.cursor import Cursor

from momapper.cursor import DecoratedCursor


def test_decorated_cursor_next(mongo_client, monkeypatch):
    with monkeypatch.context() as m:
        _map_result, _next_result = object(), object()
        m.setattr(DecoratedCursor, "_map_document", MagicMock(return_value=_map_result))
        m.setattr(Cursor, "next", MagicMock(return_value=_next_result))
        cursor = DecoratedCursor(collection=mongo_client.db[mongo_client.collection], filter={})
        assert cursor.next() is _map_result
        DecoratedCursor._map_document.assert_called_with(_next_result)
        Cursor.next.assert_called()


@pytest.mark.parametrize("document", [{"field": "value"}, None])
def test_decorated_cursor_map_document(mongo_client, monkeypatch, document):
    class TestImpl:
        def __init__(self, _document):
            self.document = document

    with monkeypatch.context() as m:
        m.setattr(DecoratedCursor, "collection", MagicMock())
        DecoratedCursor.collection._impl = TestImpl
        cursor = DecoratedCursor(collection=mongo_client.db[mongo_client.collection], filter={})
        result = cursor._map_document(document)
        if document:
            assert isinstance(result, TestImpl)
            assert result.document is document
        else:
            assert result is None


def test_decorated_cursor_first(mongo_client, monkeypatch):
    with monkeypatch.context() as m:
        _result = object()
        m.setattr(DecoratedCursor, "__getitem__", MagicMock(return_value=_result))
        cursor = DecoratedCursor(collection=mongo_client.db[mongo_client.collection], filter={})
        assert cursor.first() is _result
        DecoratedCursor.__getitem__.assert_called_with(0)


def test_decorated_cursor_first_novalue(mongo_client, monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(DecoratedCursor, "__getitem__", MagicMock(side_effect=IndexError))
        cursor = DecoratedCursor(collection=mongo_client.db[mongo_client.collection], filter={})
        assert cursor.first() is None
        DecoratedCursor.__getitem__.assert_called_with(0)
