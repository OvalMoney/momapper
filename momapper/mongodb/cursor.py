from pymongo.cursor import Cursor


class MappedCursor(Cursor):
    """Cursor implementation that maps its result to mapped objects."""

    def _map_document(self, document):
        """Maps a document to a mapped object instance.

        The class to map the document to is taken from the ``MappedCollection._impl``
        property.

        :param document: the document to map.
        :type document: dict
        """
        return self.collection._impl(_document=document) if document else None

    def next(self):
        """Overridden to map every outgoing documents to a mapped object."""
        return self._map_document(super().next())

    __next__ = next

    def first(self):
        """Helper to return the first mapped document matched by a Cursor, if any."""
        try:
            return self[0]
        except IndexError:
            return None
