from decimal import Decimal

import pytest
from bson import Decimal128

from momapper import MappedClass, Field
from momapper.mongodb.collection import MappedCollection
from momapper.types import DecimalType


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
