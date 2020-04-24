from pymongo.collection import Collection

from momapper.decorated_cursor import DecoratedCursor


class DecoratedCollection(Collection):
    """Decorated collection that generates decorated cursors.

    Subclass of :py:class:`pymongo.collection.Collection` decorated so that
    queries will return instances of a mapped class instead of plain dictionaries.

    :param impl: the class to map the returned documents to.
    :type impl: type[MappedClass]
    """

    def __init__(self, *args, impl, **kwargs):
        self._impl = impl
        super().__init__(*args, **kwargs)

    def insert_one(self, document, *args, _skip_validation=False, **kwargs):
        """Allows insert_one to be called with a MappedClass instance.

        Can be called both as the standard pymongo `insert_one` with a dictionary
        as `document`, or with an instance of :py:attr`DecoratedCollection._impl`.
        In case a dictionary is passed, validation will be performed on it, unless
        the parameter ``_skip_validation`` is passed to ``False``.

        :param document: the document to insert
        :type document: dict or MappedClass
        :param _skip_validation: whether the validation should be skipped. Default to ``False``.
        :type _skip_validation: bool
        """
        if isinstance(document, self._impl):
            document = document._document
        elif not _skip_validation:
            document = self._impl.validate(document)
        result = super().insert_one(document, *args, **kwargs)
        document["_id"] = result.inserted_id
        return result

    def find(self, *args, _skip_validation=False, **kwargs):
        """Overridden to return a decorated cursor.

        Will return a :py:class:`DecoratedCursor` that automatically instantiates
        a mapped object from a returned document, when consumed.

        :param _skip_validation: when `True`, will return a standard cursor instead.
        :type _skip_validation: bool
        """
        if _skip_validation:
            return super().find(*args, **kwargs)
        return DecoratedCursor(self, *args, **kwargs)
