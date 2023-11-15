"""Module for testing sorting tasks"""
import sys
import pytest
import mock

import pyalgotask.main as pyAlgoTask
from pyalgotask.tasks import task_base
from pyalgotask.structures.operation import OperationType

__CATEGORY__ = "tree"
__TASK_NAMES__ = [
    "bst",
    "avl",
    #"rbt",
]

__EXAMPLE_INCORRECT_TREE_INPUTS__ = ["", "0:1,5,7", "+a,+b,-a"]


def input_argument(task: str, input_array: str):
    """Generates a cli command with input"""
    return [
        "pyAlgoTask",
        __CATEGORY__,
        task,
        "-i",
        input_array,
        "-eexercise",
        "-ssolution",
    ]


def random_argument(task):
    """Generates a cli command with randomization"""
    return ["pyAlgoTask", __CATEGORY__, task, "-eexercise", "-ssolution"]


class TestSorting:
    """Class for testing Tree Algorithms"""

    @pytest.mark.parametrize("task_name", __TASK_NAMES__)
    @pytest.mark.parametrize("input_array", __EXAMPLE_INCORRECT_TREE_INPUTS__)
    @pytest.mark.timeout(2)
    def test_exception_input_all(self, task_name, input_array):
        """tests various forbidden input data"""
        with mock.patch("sys.argv", input_argument(task_name, input_array)):
            with pytest.raises(SystemExit) as pytext_sysexit:
                pyAlgoTask.main()
            assert pytext_sysexit.value.code == 2, (
                f"The argument {sys.argv} should have exited the program with code 2, "
                f"but it was {pytext_sysexit.value.code}."
            )

    def tree_collect(self, root, s):
        """collects all elements in root to set s"""
        if root.is_nil():
            return s
        s.add(root.value)
        self.tree_collect(root.left, s)
        self.tree_collect(root.right, s)
        return s

    def is_search_tree(self, node):
        """checks if root is a binary search tree"""
        if node.is_nil():
            return True
        return (node.left.is_nil() or node.left.value < node.value) \
            and (node.right.is_nil() or node.value <= node.right.value) \
            and self.is_search_tree(node.left) \
            and self.is_search_tree(node.right)

    def is_balanced(self, root):
        """Checks if root is AVL-balanced"""
        depth = {}
        def compute_depth(node):
            if node.is_nil():
                depth[node] = 0
            else:
                compute_depth(node.left)
                compute_depth(node.right)
                depth[node] = max(depth[node.left], depth[node.right]) + 1
        compute_depth(root)

        def check_depth(node):
            if node.is_nil():
                return True
            return depth[node.left] - depth[node.right] < 2 \
                and depth[node.left] - depth[node.right] > -2 \
                and check_depth(node.left) \
                and check_depth(node.right)
        return check_depth(root)

    def is_red_black(self, root):
        """TODO"""

    def is_black_balanced(self, root):
        """TODO"""

    def is_tree_for_task(self, task_name, content, root):
        """Tests if the tree root is a tree corresponding to task_name with input"""
        result = True
        if task_name == "bst":
            result &= self.tree_collect(root, set()) == content
            result &= self.is_search_tree(root)
        elif task_name == "avl":
            result &= self.tree_collect(root, set()) == content
            result &= self.is_search_tree(root)
            result &= self.is_balanced(root)
        elif task_name == "rbt":
            result &= self.tree_collect(root, set()) == content
            result &= self.is_search_tree(root)
            result &= self.is_red_black(root)
            result &= self.is_black_balanced(root)
        return result

    @pytest.mark.parametrize(
        "task_name",
        __TASK_NAMES__,
    )
    @pytest.mark.timeout(2)
    def test_random_all(self, task_name):
        """tests randomization"""
        with mock.patch("sys.argv", random_argument(task_name)):
            task = task_base.get_task_by_cmd("tree", task_name)
            try:
                pyAlgoTask.main()
            except Exception as exc:  # pylint: disable=broad-exception-caught
                assert (
                    False
                ), f'The argument {sys.argv} on input {task.task_io.randomizer.last_result} \
                    raised the exception "{exc}" but should not have.'
            values = set()
            for (root, operation) in task.algorithm():
                if operation.is_operation_type(OperationType.INSERT):
                    values.add(operation.value)
                elif operation.is_operation_type(OperationType.DELETE):
                    values.remove(operation.value)
                assert self.is_tree_for_task(task_name, values, root)
