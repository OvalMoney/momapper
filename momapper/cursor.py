class DecoratedCursor:
    def __init__(self, cursor, impl):
        self.__cursor = cursor
        self.__impl = impl

    def __getattr__(self, attr):
        return getattr(self.__cursor, attr)

    def next(self):
        document = self.__cursor.next()
        return self.__impl(_document=document) if document else None

    def __getitem__(self, index):
        result = self.__cursor[index]
        if isinstance(index, int):
            return self.__impl(_document=result) if result else None
        return result

    __next__ = next

    def first(self):
        try:
            return self[0]
        except IndexError:
            return None
