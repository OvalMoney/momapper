from momapper.fields import Field


class ValidatorMeta(type):
    """Metaclass that provides the machinery to perform schema validation.

    Will instantiate a class that uses it as metaclass, setting its ``__fields__``
    attribute to be a map of all the object attributes to their corresponding
    field names on the document being mapped by it.

    ``__fields__`` will be populated using all the attributes of the class that
    are instances of ``Field``.
    """

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
    """Base class that implements schema mapping for documents.

    All the attributes defined as instances of ``Field`` will be used
    to generate the schema of the document and to perform validation.
    """

    __fields__ = {}

    def __init__(self, _document=None, **kwargs):
        """Initializer of mapped objects.

        Can be initialized in two ways:
         - with a document already built, which will be validated.
         - with a series of keyword arguments, which will be used to build a document,
           on which validation will be performed.

        :param _document: a document already built.
        :type _document: dict
        :param kwargs: the keyword arguments used to build a document.
        :type kwargs: dict
        """
        if not _document:
            _document = self.make_document(**kwargs)
        self._document = self.validate(_document)
        super().__init__()

    @classmethod
    def make_document(cls, **kwargs):
        """Creates a document based on the given keyword arguments.

        It's as easy as building a dictionary from keywords, but with the
        keys mapped according to the schema declared by the class.

        :param kwargs: the keyword arguments used to build the document.
        :type kwargs: dict
        """
        _document = {}
        for field, value in kwargs.items():
            _document[cls.__fields__[field]] = value
        return _document

    @classmethod
    def validate(cls, document):
        """Validates a document schema and field types.

        :param document: a document already built.
        :type document: dict
        """
        _validated = {}
        for attrname, doc_attrname in cls.__fields__.items():
            _field = getattr(cls, attrname)
            _validated[doc_attrname] = _field.validate(document.get(doc_attrname))
        return _validated
