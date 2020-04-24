from pymongo.collection import Collection

from momapper.cursor import DecoratedCursor


class DecoratedCollection(Collection):
    def __init__(self, *args, impl, **kwargs):
        self._impl = impl
        super().__init__(*args, **kwargs)

    def insert_one(self, document, *args, _skip_validation=False, **kwargs):
        if isinstance(document, self._impl):
            document = document._document
        elif not _skip_validation:
            document = self._impl.validate(document)
        result = super().insert_one(document, *args, **kwargs)
        document["_id"] = result.inserted_id
        return result

    def find(self, *args, _skip_validation=False, **kwargs):
        if _skip_validation:
            return super().find(*args, **kwargs)
        return DecoratedCursor(self, *args, **kwargs)
