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
    __fields__ = {}

    def __init__(self, _document=None, **kwargs):
        if not _document:
            _document = self.make_document(**kwargs)
        self._document = self.validate(_document)

    @classmethod
    def make_document(cls, **kwargs):
        _document = {}
        for field, value in kwargs.items():
            _document[cls.__fields__[field]] = value
        return _document

    @classmethod
    def validate(cls, document):
        _validated = {}
        for attrname, doc_attrname in cls.__fields__.items():
            _field = getattr(cls, attrname)
            _validated[doc_attrname] = _field.validate(document.get(doc_attrname))
        return _validated
