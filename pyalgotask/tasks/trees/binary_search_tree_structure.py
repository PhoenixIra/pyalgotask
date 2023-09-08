"""Classes implementing the basic binary search tree"""
from abc import ABC, abstractmethod
from ... import exceptions


class BinarySearchTree(ABC):
    """
    Abstract class for binary search tree nodes
    """

    @property
    @abstractmethod
    def left(self):
        """:return: Left subtree of the tree"""

    @left.setter
    @abstractmethod
    def left(self, value):
        """:param value: Sets the left subtree of the tree"""

    @property
    @abstractmethod
    def right(self):
        """:return: Right subtree of the tree"""

    @right.setter
    @abstractmethod
    def right(self, value):
        """:param value: Sets the right subtree of the tree"""

    @property
    @abstractmethod
    def parent(self):
        """:return: parent of the node"""

    @parent.setter
    @abstractmethod
    def parent(self, value):
        """:param value: Sets the parent of the node"""

    @property
    @abstractmethod
    def value(self):
        """:return: value of the node"""

    @value.setter
    @abstractmethod
    def value(self, value):
        """:param value: Sets the value of the node"""

    @abstractmethod
    def is_nil(self):
        """Whether the node is a nil node

        :return: true if it is a nil node, else false"""

    @abstractmethod
    def is_root(self):
        """Whether this node is the root of the tree

        :return: true if the node is the root, else false"""

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class NilNode(BinarySearchTree):
    """
    Class representing a nil node of a tree
    """

    def is_nil(self):
        return True

    def is_root(self):
        return False

    def __repr__(self):
        return ""

    def __str__(self):
        return "Nil"

    @property
    def left(self):
        raise exceptions.WrongAlgorithmImplementationError(
            "Nil nodes have no left subtree"
        )

    @left.setter
    def left(self, value):
        pass

    @property
    def right(self):
        raise exceptions.WrongAlgorithmImplementationError(
            "Nil nodes have no right subtree"
        )

    @right.setter
    def right(self, value):
        pass

    @property
    def parent(self):
        raise exceptions.WrongAlgorithmImplementationError("Nil nodes have no parents")

    @parent.setter
    def parent(self, value):
        pass

    @property
    def value(self):
        raise exceptions.WrongAlgorithmImplementationError("Nil nodes have no value")

    @value.setter
    def value(self, value):
        pass


class Node(BinarySearchTree):
    """
    Class representing a regular node of a tree

    :ivar left: the left subtree of the node
    :ivar right: the right subtree of the node
    :ivar parent: the parent node of this node
    :ivar value: the value stored in this node"""

    def __init__(self, value) -> None:
        """
        Initialized the node as an tree consisting only of this node with the given value.

        :param value: the value of the node
        """
        super().__init__()
        self._left = NilNode()
        self._right = NilNode()
        self._parent = NilNode()
        self._value = value

    def is_nil(self):
        return False

    def is_root(self):
        return self.parent.is_nil()

    def __repr__(self):
        return "[" + repr(self.value) + repr(self.left) + repr(self.right) + "]"

    def __str__(self):
        return "[ Node " + str(self.value) + str(self.left) + str(self.right) + "]"

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def max(self):
        """the maximum of this subtree

        :return: the most right node in the subtree"""
        current = self
        while not current.right.is_nil():
            current = current.right
        return current

    def min(self):
        """the minimum of this subtree

        :return: the most left node in the subtree"""
        current = self
        while not current.left.is_nil():
            current = current.left
        return current

    def right_rotate(self):
        """Rotates self to the right"""
        if self.left.is_nil():
            raise exceptions.WrongAlgorithmImplementationError(
                "Right rotate on a node that does not have a left node!"
            )
        new_root = self.left
        new_right_left = self.left.right

        new_root.parent = self.parent
        new_root.right = self
        self.parent = new_root
        self.left = new_right_left
        new_right_left.parent = self

    def left_rotate(self):
        """Rotates self to the left"""
        if self.right.is_nil():
            raise exceptions.WrongAlgorithmImplementationError(
                "Left rotate on a node that does not have a right node!"
            )
        new_root = self.right
        new_left_right = self.right.left

        new_root.parent = self.parent
        new_root.left = self
        self.parent = new_root
        self.right = new_left_right
        new_left_right.parent = self
