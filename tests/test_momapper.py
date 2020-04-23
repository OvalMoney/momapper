#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `momapper` package."""

import pytest
from pymongo.results import InsertOneResult

from momapper import collection, MongoManager, MappedClass, Field

from bson import ObjectId
from pymongo import MongoClient


class Document(MappedClass):
    uid = Field("_id", ObjectId, if_missing=ObjectId)
    name = Field("name", str)
    money = Field("amount_of_money", int)

    def __repr__(self):
        return f"<Document {self.__dict__}>"


@pytest.fixture(scope="session")
def mongo_client():
    client = MongoClient()
    db = client.get_database("testing")
    return db


@pytest.fixture
def register_documents(monkeypatch, mongo_client):
    with monkeypatch.context() as m:
        m.setattr(MongoManager, "_registry", {})
        MongoManager.register(Document, mongo_client.documents)
        yield


@pytest.fixture
def document(register_documents):
    return Document(name="walter", money=1000)


def test_insert_one(document):
    result = collection(Document).insert_one(document)
    assert isinstance(result, InsertOneResult)
    assert collection(Document).find_one({"_id": result.inserted_id})


def test_insert_one_no_validation(register_documents):
    invalid_document = {"invalid": "doc"}
    result = collection(Document).insert_one(invalid_document, _skip_validation=True)
    assert isinstance(result, InsertOneResult)
    assert collection(Document).find_one(
        {"_id": result.inserted_id}, _skip_validation=True
    )


def test_insert_one_validation(register_documents):
    document = {"name": "walter", "amount_of_money": 10}
    result = collection(Document).insert_one(document)
    assert isinstance(result, InsertOneResult)
    assert collection(Document).find_one({"_id": result.inserted_id})


@pytest.mark.parametrize("name, money", [("walter", 100), ("gianni", -10)])
def test_find_one(document, name, money):
    document.name = name
    document.money = money
    collection(Document).insert_one(document)
    result = collection(Document).find_one({"_id": document.uid})
    assert isinstance(result, Document)
    assert result.name == name
    assert result.money == money


@pytest.mark.parametrize("name, money", [("walter", 100), ("gianni", -10)])
def test_find(document, name, money):
    document.name = name
    document.money = money
    collection(Document).insert_one(document)
    result = collection(Document).find({"_id": document.uid}).first()
    assert isinstance(result, Document)
    assert result.name == name
    assert result.money == money


def test_find_nothing(register_documents):
    result = collection(Document).find({"nonexistent": 10}).first()
    assert result is None


def test_find_one_nothing(register_documents):
    result = collection(Document).find_one({"nonexistent": 10})
    assert result is None


def test_find_skip_validation(register_documents):
    invalid_document = {"invalid": "doc"}
    _id = (
        collection(Document)
        .insert_one(invalid_document, _skip_validation=True)
        .inserted_id
    )
    result = collection(Document).find({"_id": _id}, _skip_validation=True)[0]
    assert isinstance(result, dict)
    assert result == {"_id": _id, "invalid": "doc"}


def test_find_one_skip_validation(register_documents):
    invalid_document = {"invalid": "doc"}
    _id = (
        collection(Document)
        .insert_one(invalid_document, _skip_validation=True)
        .inserted_id
    )
    result = collection(Document).find_one({"_id": _id}, _skip_validation=True)
    assert isinstance(result, dict)
    assert result == {"_id": _id, "invalid": "doc"}
