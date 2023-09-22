"""Classes implementing the basic binary search tree"""
from abc import ABC, abstractmethod


class WrongTreeUsageError(Exception):
    """Used for when a tree is wrongly used."""


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

    @abstractmethod
    def visitor(self, visitor):
        """Visitor for the tree in postfix notation, i.e. first left, then right, then parent

        :param visitor: the method to visir
        :return: a list of return values, first of the root, then left, then right subtree
        """


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
        raise WrongTreeUsageError("Nil nodes have no left subtree")

    @left.setter
    def left(self, value):
        pass

    @property
    def right(self):
        raise WrongTreeUsageError("Nil nodes have no right subtree")

    @right.setter
    def right(self, value):
        pass

    @property
    def parent(self):
        raise WrongTreeUsageError("Nil nodes have no parents")

    @parent.setter
    def parent(self, value):
        pass

    @property
    def value(self):
        raise WrongTreeUsageError("Nil nodes have no value")

    @value.setter
    def value(self, value):
        pass

    def visitor(self, visitor):
        return None


class Node(BinarySearchTree):
    """
    Class representing a regular node of a tree

    :ivar left: the left subtree of the node
    :ivar right: the right subtree of the node
    :ivar parent: the parent node of this node
    :ivar value: the value stored in this node"""

    def __init__(
        self, value, *, left=None, right=None, parent=None, nil_class=NilNode
    ) -> None:
        """
        Initialized the node as an tree consisting only of this node with the given value.

        :param value: the value of the node
        """
        super().__init__()

        if left is None:
            self._left = nil_class()
        else:
            self._left = left

        if right is None:
            self._right = nil_class()
        else:
            self._right = right

        if parent is None:
            self._parent = nil_class()
        else:
            self._parent = parent

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
            raise WrongTreeUsageError(
                "Right rotate on a node that does not have a left node!"
            )
        new_root = self.left
        new_right_left = self.left.right

        if not self.parent.is_nil() and self.parent.left == self:
            self.parent.left = new_root
        elif not self.parent.is_nil() and self.parent.right == self:
            self.parent.right = new_root

        new_root.parent = self.parent
        new_root.right = self

        self.parent = new_root
        self.left = new_right_left

        new_right_left.parent = self
        return new_root

    def left_rotate(self):
        """Rotates self to the left"""
        if self.right.is_nil():
            raise WrongTreeUsageError(
                "Left rotate on a node that does not have a right node!"
            )
        new_root = self.right
        new_left_right = self.right.left

        if not self.parent.is_nil() and self.parent.left == self:
            self.parent.left = new_root
        elif not self.parent.is_nil() and self.parent.right == self:
            self.parent.right = new_root

        new_root.parent = self.parent
        new_root.left = self

        self.parent = new_root
        self.right = new_left_right

        new_left_right.parent = self
        return new_root

    def visitor(self, visitor):
        left_ret = self.left.visitor(visitor)
        right_ret = self.right.visitor(visitor)
        root_ret = visitor(self)
        return (root_ret, left_ret, right_ret)


class AVLTree(BinarySearchTree):
    """Abstract class representing nodes of an AVL Tree

    :ivar depth: the depth of the current Node"""

    @property
    @abstractmethod
    def depth(self):
        """:return: the depth of this node"""

    @depth.setter
    @abstractmethod
    def depth(self, depth):
        """:ivar depth: the depth to set this node to"""

    @abstractmethod
    def recalculate_depth(self):
        """recalculates the depth value of this node based of its children"""
        self.depth = max(self.left.depth, self.right.depth) + 1


class AVLNil(NilNode, AVLTree):
    """Nil node with fixed balancing"""

    @property
    def depth(self):
        return -1

    @depth.setter
    def depth(self, depth):
        raise WrongTreeUsageError("NilNodes balance cannot be overwritten")

    def recalculate_depth(self):
        pass


class AVLNode(Node, AVLTree):
    """
    Class representing an AVL Tree node

    :ivar left: the left subtree of the node
    :ivar right: the right subtree of the node
    :ivar parent: the parent node of this node
    :ivar value: the value stored in this node
    :ivar balancing: the balancing value of this node"""

    def __init__(self, value, *, left=None, right=None, parent=None, depth=0) -> None:
        """
        Initialized the node as an tree consisting only of this node with the given value.

        :param value: the value of the node
        """
        super().__init__(value, left=left, right=right, parent=parent, nil_class=AVLNil)

        self._depth = depth

    def __repr__(self):
        return " ".join(
            [
                "[ Node",
                repr(self.value),
                f" d={self._depth}",
                repr(self.left),
                repr(self.right),
                "]",
            ]
        )

    def __str__(self):
        return " ".join(
            [
                "[ Node",
                str(self.value),
                f" d={self._depth}",
                str(self.left),
                str(self.right),
                "]",
            ]
        )

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth):
        self._depth = depth

    def recalculate_depth(self):
        """recalculates the depth value of this node based of its children"""
        self.depth = max(self.left.depth, self.right.depth) + 1
