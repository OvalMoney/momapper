from momapper.collection import DecoratedCollection


class MongoManager:
    _registry = {}

    @classmethod
    def register(cls, _class, collection):
        cls._registry[_class] = DecoratedCollection(collection=collection, impl=_class)

    @classmethod
    def get_collection(cls, _class):
        return cls._registry[_class]


def collection(mappedclass):
    return MongoManager.get_collection(mappedclass)
