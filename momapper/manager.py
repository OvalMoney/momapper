from momapper.collection import DecoratedCollection


class MongoManager:
    __registry = {}

    @classmethod
    def register(cls, _class, collection):
        cls.__registry[_class] = DecoratedCollection(collection=collection, impl=_class)

    @classmethod
    def get_collection(cls, _class):
        return cls.__registry[_class]


def collection(mappedclass):
    return MongoManager.get_collection(mappedclass)
