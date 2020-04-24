from collections import namedtuple

import pytest
from pymongo import MongoClient


@pytest.fixture(scope="session")
def mongo_client():
    Client = namedtuple("Client", "db,collection")
    client = MongoClient()
    db = client.get_database("momapper_test")
    return Client(db, "momapper_test")
