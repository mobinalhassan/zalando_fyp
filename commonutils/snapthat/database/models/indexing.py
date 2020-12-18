from enum import Enum
from abc import ABC, abstractmethod


class IndexOrder(Enum):
    ASCENDING = 1
    DESCENDING = -1


class DatabaseIndex:
    def __init__(self, background = True):
        self.background = None

        self.set_background(background)

    def is_background(self):
        return self.background

    def set_background(self, background):
        self.background = bool(background)

    @abstractmethod
    def is_unique(self):
        return False

    @abstractmethod
    def get_name(self):
        """
        Returns:
            str: returns the name of the index
        """
        return ""

    @abstractmethod
    def toDBIndex(self):
        """Converts index to database specific representation"""
        pass

    @abstractmethod
    def get_fields(self):
        """Gets the list of field names involved in making the index

        Returns:
              list[str]: returns the list of field names
        """
        pass


class AbsSingleFieldIndex(DatabaseIndex):
    def __init__(self, background = True):
        super().__init__(background=background)

    @abstractmethod
    def add_field(self, field_name, unique):
        pass

class AbsCompositeIndex(DatabaseIndex):
    def __init__(self, unique = False, background= True):
        super().__init__(background)
        self.unique = None
        self.set_unique(unique)

    def set_unique(self, unique):
        unique = bool(unique)
        self.unique = unique

    def is_unique(self):
        return self.unique

    @abstractmethod
    def add_field(self, field, index_order):
        pass

class FieldIndex(AbsSingleFieldIndex):
    def __init__(self, field_name=None, unique = False, background=True):
        super().__init__(background=background)
        self.field_name = field_name
        self.unique = unique
        pass

    def get_name(self):
        name = str(self.field_name)
        if self.unique:
            name += "_unique"
        name += "_index"

        return name

    def add_field(self, field_name, unique =False):
        """set the field name to be indexed

        Args:
            field_name (str):

        Returns:

        """

        self.field_name = field_name
        self.unique = unique

    def is_unique(self):
        return self.unique

    def toDBIndex(self):
        return self.field_name

    def get_fields(self):
        return [self.field_name]

class CompositeIndex(AbsCompositeIndex):
    def __init__(self, unique=False, background = True):
        super().__init__(unique=unique,background=background)
        self.index = []

    def get_name(self):
        name = ""
        for i, (index_name, index_order) in enumerate(self.index):
            if i==0:
                name += str(index_name)
            else:
                name += "_" + str(index_name)

        if self.is_unique():
            name += "_unique"
        name += "_index"

        return name


    def add_field(self, field_name, index_order):
        """adds a field to the composite index

        Args:
            field_name (str): the field name in the composite index
            index_order (IndexOrder): enumeration of index order

        Returns:

        """

        order = int(index_order.value)
        key = (field_name, order)
        self.index.append(key)

    def toDBIndex(self):
        return self.index

    def get_fields(self):
        fields = []
        for field_name,  _ in self.index:
            fields.append(field_name)

        return fields

