from decimal import Decimal

import pytest

from momapper import MappedClass, Field
from momapper.mongodb.collection import MappedCollection
from momapper.types import DecimalType


@pytest.mark.parametrize("amount", [0, 0.0, Decimal("10")])
def test_decimal_type(mongo_client, amount):
    class DocWithDecimal(MappedClass):
        amount = Field("amount", type_=DecimalType)

    doc = DocWithDecimal(amount=amount)
    assert isinstance(doc.amount, Decimal)

    collection = MappedCollection(mongo_client.db, mongo_client.collection, impl=DocWithDecimal)
    doc_id = collection.insert_one(doc).inserted_id
    fetched_doc = collection.find_one({"_id": doc_id})
    assert isinstance(fetched_doc.amount, Decimal)

    assert doc.amount == fetched_doc.amount
