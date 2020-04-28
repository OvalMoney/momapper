=====
Usage
=====

To use MoMapper in a project, first you need to declare your schema::

    from momapper import collection, MongoManager, MappedClass, Field
    from momapper.types import ObjectIdType, StringType, IntType

    from pymongo import MongoClient
    from bson import ObjectId


    class Document(MappedClass):
        uid = Field("_id", ObjectIdType, if_missing=ObjectId, required=True)
        name = Field("name", StringType)
        money = Field("amount_of_money", IntType)

        def __repr__(self):
            return f"<Document {self.__dict__}>"

Then you need to register the mapped class to a collection, through the ``MongoManager``::

    MongoManager.register(
        Document,
        database=MongoClient().get_database(),
        collection_name="documents"
    )

And then you can start using your mapped documents with MongoDB, using the same API of ``pymongo.collection.Collection``::

    >>> document = Document(name="walter", money=1000)
    >>> oid = collection(Document).insert_one(document).inserted_id
    >>> collection(Document).find_one(oid)
    <Document {"_id": ObjectId(), "name": "walter", "money": 1000)

You can also create a document by passing a dictionary as argument::

    >>> Document({"name": "walter", "money": 1000})
    <Document {"_id": ObjectId(), "name": "walter", "money": 1000)

Validation is performed at init time::

    >>> Document(name="walter", money="a lot")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/walter/Work/momapper/project/momapper/mappedclass.py", line 52, in __init__
        self._document = self.validate(_document)
      File "/Users/walter/Work/momapper/project/momapper/mappedclass.py", line 79, in validate
        _validated[doc_attrname] = _field.validate(document.get(doc_attrname))
      File "/Users/walter/Work/momapper/project/momapper/fields.py", line 77, in validate
        validator.validate()
      File "/Users/walter/Work/momapper/project/momapper/types.py", line 77, in validate
        raise ValidationError
    momapper.types.ValidationError
