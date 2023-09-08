"""Task for inserting or deleting in regular binary search trees"""

from pyalgotask.tasks import task_base
from pyalgotask.tasks.trees.tree_base import Tree

from pyalgotask.structures.binary_search_tree import Node, NilNode
from pyalgotask.structures.operation import OperationType

from pyalgotask import language as lang


class BinarySearchTree(Tree):
    """
    Binary Search Trees as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 312-325

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar operation: operations to execute on the tree"""

    def __init__(self):
        super().__init__()
        self.exercise_texts = [
            lang.get_text("tree", "binary_search_tree_prefix"),
            lang.get_text("tree", "binary_search_tree_postfix"),
        ]
        self.cmd_info = task_base.TaskCmd(
            "bst",
            "Task to insert and delete into a binary search tree",
            "Insert/delete in binary search tree",
        )

    def init_tree_argument_parser(self, parser):
        pass

    def tree_parse(self, arg_input) -> None:
        pass

    def insert(self, node, value):
        """Performs an insert of the value to the tree

        :param node: the root of the tree to insert into
        :param value: the value to insert
        :return: the tree with the value inserted
        """
        current = node
        parent = NilNode()

        while not current.is_nil():
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        new_node = Node(value, parent=parent)

        if parent.is_nil():
            return new_node

        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        return node

    def transplant(self, root, node_to, node_from):
        """Transplants node_from into _node_to

        :param root: root of the tree
        :param node_to: the node to replace
        :param node_from: the node to insert
        :return: the new root of the tree"""
        if node_to.parent.is_nil():
            root = node_from
        elif node_to == node_to.parent.left:
            node_to.parent.left = node_from
        else:
            node_to.parent.right = node_from

        if not node_from.is_nil():
            node_from.parent = node_to.parent

        return root

    def search(self, root, value):
        """Searches a value from the tree rooted at root and returns it

        :param root: root of the tree
        :param value: value to search for
        :return: node with value"""
        current = root
        while not current.is_nil() and value != current.value:
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return current

    def delete(self, root, value):
        """Performs a delete of the value from the tree

        :param node: the root of the tree to delete from
        :param value: the value to delete
        :return: the tree with the value deleted"""

        node = self.search(root, value)

        if node.is_nil():
            raise ValueError(
                f"Tried to delete value {value} not present in tree {root}"
            )

        if node.left.is_nil():
            return self.transplant(root, node, node.left)

        if node.right.is_nil():
            return self.transplant(root, node, node.right)

        min_tree = node.right.min()
        if min_tree != node.right:
            root = self.transplant(root, min_tree, min_tree.right)
            min_tree.right = node.right
            min_tree.right.parent = min_tree

        root = self.transplant(root, node, min_tree)
        min_tree.left = node.left
        min_tree.left.parent = min_tree

        return root

    def algorithm(self):
        """Generates a tree following the operations

        We use singleton list as tree in order to make a lightweight pointer to the root nodes

        :yield: intermediate steps"""
        root = NilNode()

        for operation in self.operations:
            if operation.is_operation_type(OperationType.INSERT):
                root = self.insert(root, operation.value)
            elif operation.is_operation_type(OperationType.DELETE):
                root = self.delete(root, operation.value)
            else:
                raise NotImplementedError(
                    f"Operator {operation.type} not supported by task {self.__class__.__name__}"
                )
            yield (root, str(operation))


task_base.register_task("tree", BinarySearchTree())
