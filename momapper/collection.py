from momapper.cursor import DecoratedCursor


class DecoratedCollection:
    def __init__(self, collection, impl):
        self.__collection = collection
        self.__impl = impl

    def __getattr__(self, attr):
        return getattr(self.__collection, attr)

    def insert_one(self, document, *args, _skip_validation=False, **kwargs):
        if isinstance(document, self.__impl):
            document = document._document
        elif not _skip_validation:
            document = self.__impl.validate(document)._document
        result = self.__collection.insert_one(document, *args, **kwargs)
        document["_id"] = result.inserted_id
        return result

    def find(self, *args, _skip_validation=False, **kwargs):
        _cursor = self.__collection.find(*args, **kwargs)
        if _skip_validation:
            return _cursor
        return DecoratedCursor(_cursor, self.__impl)

    def find_one(self, *args, _skip_validation=False, **kwargs):
        document = self.__collection.find_one(*args, **kwargs)
        if _skip_validation:
            return document
        return self.__impl(_document=document) if document else None
