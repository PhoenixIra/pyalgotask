"""Task for inserting or deleting in regular binary search trees"""

from pyalgotask.tasks import task_base
from pyalgotask.tasks.trees.binary_search_tree import BinarySearchTree

from pyalgotask.structures.binary_search_tree import AVLNode, AVLNil
from pyalgotask.structures.operation import OperationType

from pyalgotask import language as lang


class AVLTree(BinarySearchTree):
    """
    Adelson-Velsky and Landis Trees (short: AVL Trees) inspired by
    Donald E. Knuth. The Art of Computer Programming Volume 3:
    Sorting and Searching

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar operation: operations to execute on the tree"""

    def __init__(self):
        super().__init__()
        self.exercise_texts = [
            lang.get_text("tree", "avl_tree_prefix"),
            lang.get_text("tree", "avl_tree_postfix"),
        ]
        self.cmd_info = task_base.TaskCmd(
            "avl",
            "Task to insert and delete into an avl tree",
            "Insert/delete in avl tree",
        )

    def init_tree_argument_parser(self, parser):
        pass

    def tree_parse(self, arg_input) -> None:
        pass

    def insert(self, value):
        """Performs an insert of the value to the tree

        :param value: the value to insert
        :return: the tree with the value inserted
        """
        # Initialize (A1)
        current = self.algorithm_root
        parent = AVLNil()

        # Compare, Move left and Move right (A2, A3, A4)
        while not current.is_nil():
            parent = current
            if value < current.value:
                new_current = current.left
            else:
                new_current = current.right

            current = new_current

        # Initialize (A5)
        new_node = AVLNode(value, parent=parent)

        if parent.is_nil():
            self.algorithm_root = new_node
            return

        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        # balance adjust (A6)
        self.adjust_depth(new_node.parent)

        # rebalance (A7-A9)
        root = self.balance(new_node)
        self.algorithm_root = root

    def adjust_depth(self, node):
        """adjusts the depth values starting from node

        :param node: the inserted node"""
        # Adjust balancing (A6)
        current = node
        while not current.is_nil():
            current.recalculate_depth()
            current = current.parent

    def balance_left(self, current):
        """Balances a left imbalance of current

        :param current: the node to balance
        :return: the new root of the subtree"""
        left = current.left
        if left.left.depth >= left.right.depth:
            # left leaning or balanced
            current = current.right_rotate()

            current.right.recalculate_depth()
            current.recalculate_depth()
        else:
            # left right leaning
            left.left_rotate()
            current = current.right_rotate()

            current.left.recalculate_depth()
            current.right.recalculate_depth()
            current.recalculate_depth()

        return current

    def balance_right(self, current):
        """Balances a right imbalance of current

        :param current: the node to balance
        :return: the new root of the subtree"""
        right = current.right
        if right.left.depth <= right.right.depth:
            # right leaning or balanced
            current = current.left_rotate()

            current.left.recalculate_depth()
            current.recalculate_depth()
        else:
            # right left leaning
            right.right_rotate()
            current = current.left_rotate()

            current.left.recalculate_depth()
            current.right.recalculate_depth()
            current.recalculate_depth()

        return current

    def balance(self, node):
        """
        Balances according to the balances in the tree starting from node.
        Since it only fixed -2 and +2, it will only fix where needed

        :return: the new root of the tree
        """
        if node.is_nil():
            return node

        child = node
        current = node.parent
        while not current.is_nil():
            if current.left.depth == current.right.depth + 2:
                # left imbalance
                current = self.balance_left(current)
            if current.left.depth == current.right.depth - 2:
                # right imbalance
                current = self.balance_right(current)

            child = current
            current = current.parent

        return child

    def delete(self, value):
        """Performs a delete of the value from the tree
        :param value: the value to delete
        :return: the tree with the value deleted"""

        node = self.search(value)

        if node.is_nil():
            raise ValueError(
                f"Tried to delete value {value} not present in tree {self.algorithm_root}"
            )

        if node.left.is_nil():
            removed_in_node = node.parent
            self.transplant(node, node.right)

        elif node.right.is_nil():
            removed_in_node = node.parent
            self.transplant(node, node.left)

        else:
            min_tree = node.right.min()
            if min_tree != node.right:
                removed_in_node = min_tree.parent
                self.transplant(min_tree, min_tree.right)
                min_tree.right = node.right
                min_tree.right.parent = min_tree
            else:
                removed_in_node = min_tree

            self.transplant(node, min_tree)

            min_tree.left = node.left
            min_tree.left.parent = min_tree

        self.adjust_depth(removed_in_node)

        self.balance(removed_in_node)

    def algorithm(self):
        """Generates a tree following the operations

        We use singleton list as tree in order to make a lightweight pointer to the root nodes

        :yield: intermediate steps"""
        self.algorithm_root = AVLNil()

        for operation in self.operations:
            if operation.is_operation_type(OperationType.INSERT):
                self.insert(operation.value)
            elif operation.is_operation_type(OperationType.DELETE):
                self.delete(operation.value)
            else:
                raise NotImplementedError(
                    f"Operator {operation.type} not supported by task {self.__class__.__name__}"
                )
            yield (self.algorithm_root, operation)


task_base.register_task("tree", AVLTree())
