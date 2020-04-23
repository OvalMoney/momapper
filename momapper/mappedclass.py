from momapper.fields import Field


class ValidatorMeta(type):
    def __new__(mcs, name, bases, classdct):
        fields = dict()
        for attrname, cls_attr in classdct.items():
            if isinstance(cls_attr, Field):
                if not cls_attr.field:
                    cls_attr.field = attrname
                fields[attrname] = cls_attr.field

        classdct["__fields__"] = fields

        return super().__new__(mcs, name, bases, classdct)


class MappedClass(metaclass=ValidatorMeta):
    __collection_name__ = None
    __fields__ = []

    def __init__(self, _document=None, *args, **kwargs):
        self._document = _document or {}
        for field, value in kwargs.items():
            setattr(self, field, value)
        self._validate_document()

    def _validate_document(self):
        for attrname in self.__fields__:
            getattr(self, attrname)

    @classmethod
    def validate(cls, document):
        return cls(_document=document)
