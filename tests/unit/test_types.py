from decimal import Decimal

import pytest
from bson import Decimal128

from momapper import MappedClass, Field
from momapper.mongodb.collection import MappedCollection
from momapper.types import (
    DecimalType,
    ValidationError,
    IntType,
    FloatType,
    StringType,
    ByteType,
    BoolType,
    ListType,
    DictType,
)


@pytest.mark.parametrize("value, exception", [(0, None), (object(), ValidationError)])
def test_int_type(mongo_client, value, exception):
    class DocWithInt(MappedClass):
        value = Field("value", type_=IntType)

    if exception:
        with pytest.raises(exception):
            DocWithInt(value=value)
    else:
        doc = DocWithInt(value=value)
        assert doc.value == value
        assert doc._document["value"] == value
        collection = MappedCollection(
            mongo_client.db, mongo_client.collection, impl=DocWithInt
        )
        collection.insert_one(doc)


@pytest.mark.parametrize("value, exception", [(0.0, None), (object(), ValidationError)])
def test_float_type(mongo_client, value, exception):
    class DocWithFloat(MappedClass):
        value = Field("value", type_=FloatType)

    if exception:
        with pytest.raises(exception):
            DocWithFloat(value=value)
    else:
        doc = DocWithFloat(value=value)
        assert doc.value == value
        assert doc._document["value"] == value
        collection = MappedCollection(
            mongo_client.db, mongo_client.collection, impl=DocWithFloat
        )
        collection.insert_one(doc)


@pytest.mark.parametrize("amount", [0, 0.0, Decimal("10")])
def test_decimal_type(mongo_client, amount):
    class DocWithDecimal(MappedClass):
        amount = Field("amount", type_=DecimalType)

    doc = DocWithDecimal(amount=amount)
    assert isinstance(doc.amount, Decimal)
    assert isinstance(doc._document["amount"], Decimal128)

    collection = MappedCollection(
        mongo_client.db, mongo_client.collection, impl=DocWithDecimal
    )
    doc_id = collection.insert_one(doc).inserted_id
    fetched_doc = collection.find_one({"_id": doc_id})
    assert isinstance(fetched_doc.amount, Decimal)
    assert isinstance(fetched_doc._document["amount"], Decimal128)

    assert doc.amount == fetched_doc.amount


def test_decimal_type_if_missing(mongo_client):
    class DocWithDecimalRequired(MappedClass):
        amount = Field(
            "amount", type_=DecimalType, required=True, if_missing=Decimal(5)
        )

    doc = DocWithDecimalRequired()
    assert isinstance(doc.amount, Decimal)
    assert isinstance(doc._document["amount"], Decimal128)

    collection = MappedCollection(
        mongo_client.db, mongo_client.collection, impl=DocWithDecimalRequired
    )
    doc_id = collection.insert_one(doc).inserted_id
    fetched_doc = collection.find_one({"_id": doc_id})
    assert isinstance(fetched_doc.amount, Decimal)
    assert isinstance(fetched_doc._document["amount"], Decimal128)

    assert doc.amount == fetched_doc.amount


@pytest.mark.parametrize(
    "value, exception", [("value", None), (object(), ValidationError)]
)
def test_string_type(mongo_client, value, exception):
    class DocWithString(MappedClass):
        value = Field("value", type_=StringType)

    if exception:
        with pytest.raises(exception):
            DocWithString(value=value)
    else:
        doc = DocWithString(value=value)
        assert doc.value == value
        assert doc._document["value"] == value
        collection = MappedCollection(
            mongo_client.db, mongo_client.collection, impl=DocWithString
        )
        collection.insert_one(doc)


@pytest.mark.parametrize(
    "value, exception", [(b"value", None), (object(), ValidationError)]
)
def test_bytes_type(mongo_client, value, exception):
    class DocWithBytes(MappedClass):
        value = Field("value", type_=ByteType)

    if exception:
        with pytest.raises(exception):
            DocWithBytes(value=value)
    else:
        doc = DocWithBytes(value=value)
        assert doc.value == value
        assert doc._document["value"] == value
        collection = MappedCollection(
            mongo_client.db, mongo_client.collection, impl=DocWithBytes
        )
        collection.insert_one(doc)


@pytest.mark.parametrize(
    "value, exception", [(False, None), (True, None), (object(), ValidationError)]
)
def test_bool_type(mongo_client, value, exception):
    class DocWithBool(MappedClass):
        value = Field("value", type_=BoolType)

    if exception:
        with pytest.raises(exception):
            DocWithBool(value=value)
    else:
        doc = DocWithBool(value=value)
        assert doc.value == value
        assert doc._document["value"] == value
        collection = MappedCollection(
            mongo_client.db, mongo_client.collection, impl=DocWithBool
        )
        collection.insert_one(doc)


@pytest.mark.parametrize(
    "value, exception", [(["value"], None), (object(), ValidationError)]
)
def test_list_type(mongo_client, value, exception):
    class DocWithList(MappedClass):
        value = Field("value", type_=ListType)

    if exception:
        with pytest.raises(exception):
            DocWithList(value=value)
    else:
        doc = DocWithList(value=value)
        assert doc.value == value
        assert doc._document["value"] == value
        collection = MappedCollection(
            mongo_client.db, mongo_client.collection, impl=DocWithList
        )
        collection.insert_one(doc)


@pytest.mark.parametrize(
    "value, exception", [({"value": "value"}, None), (object(), ValidationError)]
)
def test_dict_type(mongo_client, value, exception):
    class DocWithDict(MappedClass):
        value = Field("value", type_=DictType)

    if exception:
        with pytest.raises(exception):
            DocWithDict(value=value)
    else:
        doc = DocWithDict(value=value)
        assert doc.value == value
        assert doc._document["value"] == value
        collection = MappedCollection(
            mongo_client.db, mongo_client.collection, impl=DocWithDict
        )
        collection.insert_one(doc)
