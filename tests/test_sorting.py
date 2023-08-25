"""Module for testing sorting tasks"""
import sys
import pytest
import mock

import pyalgotask.__main__ as pyAlgoTask
from pyalgotask.tasks import task_base

__CATEGORY__ = "sorting"
__TASK_NAMES__ = [
    "bubble",
    "insertion",
    "selection",
    "merge",
    "heap",
    "quick-lomuto",
    "quick-hoare",
    "radix",
    "bucket",
    "counting",
]

__EXAMPLE_INCORRECT_INPUTS__ = ["", "0:1,5,7", "a,b,t"]


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
    """Class for testing Sorting Algorithms"""

    @pytest.mark.parametrize("task_name", __TASK_NAMES__)
    @pytest.mark.parametrize("input_array", __EXAMPLE_INCORRECT_INPUTS__)
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

    @pytest.mark.parametrize(
        "task_name",
        __TASK_NAMES__,
    )
    @pytest.mark.timeout(2)
    def test_no_exception_random_all(self, task_name):
        """tests randomization"""
        with mock.patch("sys.argv", random_argument(task_name)):
            task = task_base.get_task_by_cmd("sorting", task_name)
            try:
                pyAlgoTask.main()
            except Exception as exc:  # pylint: disable=broad-exception-caught
                assert (
                    False
                ), f'The argument {sys.argv} on input {task.task_io.randomizer.last_result} \
                    raised the exception "{exc}" but should not have.'
            output = [task.array] + [array for (array, _) in task.algorithm()]
            assert output[-1] == sorted(task.array), (
                f"The list {task.array} was not sorted correctly by {task_name}. "
                f"Instead it gave {output[-1]}"
            )
