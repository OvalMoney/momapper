from .collection import MappedCollection


class MongoManager:
    _registry = {}

    @classmethod
    def register(cls, _class, database, collection_name, **collection_options):
        cls._registry[_class] = MappedCollection(
            database=database, name=collection_name, impl=_class, **collection_options
        )

    @classmethod
    def get_collection(cls, _class):
        return cls._registry[_class]


def collection(mappedclass):
    return MongoManager.get_collection(mappedclass)
