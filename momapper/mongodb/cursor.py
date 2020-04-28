from pymongo.cursor import Cursor


class MappedCursor(Cursor):
    def _map_document(self, document):
        return self.collection._impl(_document=document) if document else None

    def next(self):
        return self._map_document(super().next())

    __next__ = next

    def first(self):
        try:
            return self[0]
        except IndexError:
            return None
