# -*- coding: utf-8 -*-

"""Top-level package for MoMapper (Mongo Mapper)."""

__author__ = """Walter Danilo Galante"""
__email__ = "walter.galante@ovalmoney.com"
__version__ = "0.0.4"


from .fields import Field
from .mappedclass import MappedClass
from .mongodb.manager import MongoManager, collection

__all__ = ["Field", "MappedClass", "MongoManager", "collection"]
