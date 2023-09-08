"""Various datastructures used in algorithms and tasks"""
from enum import Enum, auto
from collections import namedtuple

from pyalgotask import language as lang


class OperationType(Enum):
    """
    Class for insert and delete operations as used by `pyalgotask.input.in_del_operators` and
    `pyalgotask.randomizer.in_del_operators`.
    """

    INSERT = auto()
    DELETE = auto()


class Operation(namedtuple("Operation", ["type", "value"])):
    """
    Namedtuple that offers to string method via locatisation method

    :ivar operation: the operation enum type OperationType
    :ivar value: the integer value of the operation
    """

    def is_operation_type(self, operation):
        """checks whether this is the given operation

        :param operation: check whether self is of this operation"""
        return self.type == operation

    def __repr__(self):
        """gives a string according to the language files and type

        :return: a string according to the language file"""
        if self.is_operation_type(OperationType.INSERT):
            return lang.get_text("insert-operation").format(self.value)
        if self.is_operation_type(OperationType.DELETE):
            return lang.get_text("delete-operation").format(self.value)
        raise NotImplementedError(f"The operation {self} is not supported yet")
