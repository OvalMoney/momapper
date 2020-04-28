from .collection import MappedCollection


class MongoManager:
    """Manager of MongoDB datastore.

    Gives access to MongoDB storage for registered ``momapper.MappedClass``,
    by creating and storing ``momapper.MappedCollection`` instances in the registry.
    """

    _registry = {}

    @classmethod
    def register(cls, _class, database, collection_name, **collection_options):
        """Register a MappedClass on MongoDB datastore.

        :param _class: the class to register.
        :type _class: Type[momapper.MappedClass]
        :param database: the database object from pymongo.
        :type database: pymongo.database.Database
        :param collection_name: the collection name for the mapped class.
        :type collection_name: str
        :param collection_options: the keyword arguments to pass when instantiating the ``MappedCollection``.
        :type collection_options: dict
        """
        cls._registry[_class] = MappedCollection(
            database=database, name=collection_name, impl=_class, **collection_options
        )

    @classmethod
    def get_collection(cls, _class):
        """Retrieve the mapped collection from the registry.

        :param _class: the registered mapped class.
        :type _class: Type[momapper.MappedClass]
        :return: the mapped collection for the registered class.
        :rtype: MappedCollection
        """
        return cls._registry[_class]


def collection(mappedclass):
    """Helper to simplify access to MongoDB datastore.

    :param mappedclass: the registered mapped class.
    :type mappedclass: Type[momapper.MappedClass]
    :return: the mapped collection for the registered class.
    :rtype: MappedCollection
    """
    return MongoManager.get_collection(mappedclass)
