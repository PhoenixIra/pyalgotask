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

    def insert(self, node, value):
        """Performs an insert of the value to the tree

        :param node: the root of the tree to insert into
        :param value: the value to insert
        :return: the tree with the value inserted
        """
        # Initialize (A1)
        current = node
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
            return new_node

        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        # balance adjust (A6)
        self.insert_adjust_balance(new_node)

        # rebalance (A7-A9)
        root = self.balance(new_node)

        return root

    def insert_adjust_balance(self,new_node):
        """adjusts the balance values after inserting new_nide
        
        :param new_node: the inserted node"""
        # Adjust balancing (A6)
        last = new_node
        current = new_node.parent
        while not current.is_nil():
            if current.left == last:
                # added left
                current.balance -= 1
                if current.balance == 0:
                    # height remained
                    break
            elif current.right == last:
                # added right
                current.balance += 1
                if current.balance == 0:
                    # height remained
                    break

    def balance_left(self, current):
        """Balances a left imbalance of current
        
        :param current: the node to balance
        :return: the new root of the subtree"""
        left = current.left
        if left.balance in (-1, 0):
            # left leaning or balanced
            current = current.right_rotate()
            current.balance += 1
            current.right.balance += 1
        elif left.balance == 1:
            # left right leaning
            left_right_balance = left.right.balance
            left.left_rotate()
            current = current.right_rotate()

            current.balance = 0

            # decide where the small subtree goes to
            if left_right_balance == 1:
                current.left.balance = -1
            else:
                current.left.balance = 0
            if left_right_balance == -1:
                current.right.balance = 1
            else:
                current.right.balance = 0

        return current

    def balance_right(self, current):
        """Balances a right imbalance of current
        
        :param current: the node to balance
        :return: the new root of the subtree"""
        right = current.right
        if right.balance in (0, 1):
            current = current.left_rotate()
            current.balance -= 1
            current.right.balance -= 1
        elif right.balance == -1:
            right_left_balance = right.left.balance
            right.right_rotate()
            current = current.left_rotate()

            current.balance = 0

            # decide where the small subtree goes to
            if right_left_balance == -1:
                current.left.balance = 1
            else:
                current.left.balance = 0
            if right_left_balance == 1:
                current.right.balance = -1
            else:
                current.right.balance = 0

        return current

    def balance(self, new_node):
        """
        Balances according to the balances in the tree starting from new_node. 
        Since it only fixed -2 and +2, it will only fix where needed

        :param new_node: the node inserted
        :return: the new root of the tree
        """
        last = new_node
        current = new_node.parent
        while not current.is_nil():
            if current.balance == -2:
                # left imbalance
                current = self.balance_left(current)
            if current.balance == 2:
                # right imbalance
                current = self.balance_right(current)

            last = current
            current = current.parent

        return last


    def delete_adjust_balance(self, node):
        """Adjusts the balance values of all nodes in the tree after a delete
        
        :param node: subtree which hight decreased by one"""
        last = node
        current = node.parent
        while not current.is_nil():
            if current.left == last:
                # added left
                current.balance += 1
                if current.balance == 0:
                    # height remained
                    break
            elif current.right == last:
                # added right
                current.balance -= 1
                if current.balance == 0:
                    # height remained
                    break

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
            removed_in_node = node.parent
            self.transplant(root, node, node.left)

        elif node.right.is_nil():
            removed_in_node = node.parent
            self.transplant(root, node, node.right)

        else:
            min_tree = node.right.min()
            if min_tree != node.right:
                removed_in_node = node.parent
                root = self.transplant(root, min_tree, min_tree.right)
                min_tree.right = node.right
                min_tree.right.parent = min_tree
            else:
                removed_in_node = min_tree.parent

            root = self.transplant(root, node, min_tree)
            min_tree.left = node.left
            min_tree.left.parent = min_tree

        self.delete_adjust_balance(removed_in_node)

        root = self.balance(removed_in_node)

        return root

    def algorithm(self):
        """Generates a tree following the operations

        We use singleton list as tree in order to make a lightweight pointer to the root nodes

        :yield: intermediate steps"""
        root = AVLNil()

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


task_base.register_task("tree", AVLTree())
