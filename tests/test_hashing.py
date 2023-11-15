"""Module for testing sorting tasks"""
import sys
import pytest
import mock

import pyalgotask.main as pyAlgoTask
from pyalgotask.tasks import task_base

__CATEGORY__ = "hashing"

__EXAMPLE_INCORRECT_OP_INPUTS__ = ["", "+0:1,+5,+7", "+1,-2", "+a,+b,-a", "a,b,c"]


def input_argument(task: str, arg_input: str):
    """Generates a cli command with input"""
    return [
        "pyalgotask",
        __CATEGORY__,
        task,
        "-eexercise",
        "-ssolution",
        "-i",
        arg_input,
    ]


def random_argument(task):
    """Generates a cli command with randomization"""
    return ["pyalgotask", __CATEGORY__, task, "-eexercise", "-ssolution"]


def div_argument():
    """Parameters for division method"""
    return ["--div", "8"]


def mult_argument():
    """Parameters for multiplication method"""
    return ["--mult", "0.125", "8"]


def mult_shift_argument():
    """Parameters for multiply-shift method"""
    return ["--mult-shift", "2", "3"]


__HASH_FUNCTIONS__ = [div_argument, mult_argument, mult_shift_argument]


class TestHashing:
    """Class for testing Sorting Algorithms"""

    @pytest.mark.parametrize("input_operations", __EXAMPLE_INCORRECT_OP_INPUTS__)
    @pytest.mark.parametrize("hash_function", __HASH_FUNCTIONS__)
    @pytest.mark.timeout(2)
    def test_exception_input_chaining(self, input_operations, hash_function):
        """tests various forbidden input data"""
        args = input_argument("chaining", input_operations) + hash_function()
        with mock.patch("sys.argv", args):
            with pytest.raises(SystemExit) as pytext_sysexit:
                pyAlgoTask.main()
            assert pytext_sysexit.value.code == 2, (
                f"The argument {sys.argv} should have exited the program with code 2, "
                f"but it was {pytext_sysexit.value.code}."
            )

    @pytest.mark.parametrize("input_operations", __EXAMPLE_INCORRECT_OP_INPUTS__)
    @pytest.mark.parametrize("hash_function", __HASH_FUNCTIONS__)
    @pytest.mark.timeout(2)
    def test_exception_input_linear(self, input_operations, hash_function):
        """tests various forbidden input data"""
        args = input_argument("linearprobing", input_operations) + hash_function()
        with mock.patch("sys.argv", args):
            with pytest.raises(SystemExit) as pytext_sysexit:
                pyAlgoTask.main()
            assert pytext_sysexit.value.code == 2, (
                f"The argument {sys.argv} should have exited the program with code 2, "
                f"but it was {pytext_sysexit.value.code}."
            )

    @pytest.mark.parametrize("input_operations", __EXAMPLE_INCORRECT_OP_INPUTS__)
    @pytest.mark.parametrize("hash_function", __HASH_FUNCTIONS__)
    @pytest.mark.timeout(2)
    def test_exception_input_quadratic(self, input_operations, hash_function):
        """tests various forbidden input data"""
        args = (
            input_argument("quadraticprobing", input_operations)
            + hash_function()
            + ["--constants", "2", "3"]
        )
        with mock.patch("sys.argv", args):
            with pytest.raises(SystemExit) as pytext_sysexit:
                pyAlgoTask.main()
            assert pytext_sysexit.value.code == 2, (
                f"The argument {sys.argv} should have exited the program with code 2, "
                f"but it was {pytext_sysexit.value.code}."
            )

    @pytest.mark.parametrize("input_operations", __EXAMPLE_INCORRECT_OP_INPUTS__)
    @pytest.mark.parametrize("hash_function_1", __HASH_FUNCTIONS__)
    @pytest.mark.parametrize("hash_function_2", __HASH_FUNCTIONS__)
    @pytest.mark.timeout(2)
    def test_exception_input_double(
        self, input_operations, hash_function_1, hash_function_2
    ):
        """tests various forbidden input data"""
        hash_2_args = hash_function_2()
        hash_2_args[0] = hash_2_args[0] + "2"
        args = (
            input_argument("doublehashing", input_operations)
            + hash_function_1()
            + hash_2_args
        )
        with mock.patch("sys.argv", args):
            with pytest.raises(SystemExit) as pytext_sysexit:
                pyAlgoTask.main()
            assert pytext_sysexit.value.code == 2, (
                f"The argument {sys.argv} should have exited the program with code 2, "
                f"but it was {pytext_sysexit.value.code}."
            )

    @pytest.mark.parametrize("hash_function", __HASH_FUNCTIONS__)
    @pytest.mark.timeout(2)
    def test_no_exception_random_chaining(self, hash_function):
        """tests randomization"""
        with mock.patch("sys.argv", random_argument("chaining") + hash_function()):
            try:
                with pytest.raises(SystemExit) as pytest_exit:
                    pyAlgoTask.main()
                    sys.exit(0)
                task = task_base.get_task_by_cmd("hashing", "chaining")
                assert pytest_exit.value.code == 0, (
                    f"The argument {sys.argv} on input {task.task_io.randomizer.last_result} "
                    f"exited with error code but should not have."
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                task = task_base.get_task_by_cmd("hashing", "chaining")
                assert (
                    False
                ), f'The argument {sys.argv} on input {task.task_io.randomizer.last_result} \
                    raised the exception "{exc}" but should not have.'

    @pytest.mark.parametrize("hash_function", __HASH_FUNCTIONS__)
    @pytest.mark.timeout(2)
    def test_no_exception_random_linear(self, hash_function):
        """tests randomization"""
        with mock.patch("sys.argv", random_argument("linearprobing") + hash_function()):
            try:
                with pytest.raises(SystemExit) as pytest_exit:
                    pyAlgoTask.main()
                    sys.exit(0)
                task = task_base.get_task_by_cmd("hashing", "linearprobing")
                assert pytest_exit.value.code == 0, (
                    f"The argument {sys.argv} on input {task.task_io.randomizer.last_result} "
                    f"exited with error code but should not have."
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                task = task_base.get_task_by_cmd("hashing", "linearprobing")
                assert (
                    False
                ), f'The argument {sys.argv} on input {task.task_io.randomizer.last_result} \
                    raised the exception "{exc}" but should not have.'

    @pytest.mark.parametrize("hash_function", __HASH_FUNCTIONS__)
    @pytest.mark.timeout(2)
    def test_no_exception_random_quadratic(self, hash_function):
        """tests randomization"""
        with mock.patch(
            "sys.argv",
            random_argument("quadraticprobing")
            + hash_function()
            + ["--constants", "0.5", "0.5"],
        ):
            try:
                with pytest.raises(SystemExit) as pytest_exit:
                    pyAlgoTask.main()
                    sys.exit(0)
                task = task_base.get_task_by_cmd("hashing", "quadraticprobing")
                assert pytest_exit.value.code == 0, (
                    f"The argument {sys.argv} on input {task.task_io.randomizer.last_result} "
                    f"exited with error code but should not have."
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                task = task_base.get_task_by_cmd("hashing", "quadraticprobing")
                assert (
                    False
                ), f'The argument {sys.argv} on input {task.task_io.randomizer.last_result} \
                    raised the exception "{exc}" but should not have.'

    @pytest.mark.parametrize("hash_function_1", __HASH_FUNCTIONS__)
    @pytest.mark.parametrize("hash_function_2", __HASH_FUNCTIONS__)
    @pytest.mark.timeout(2)
    def test_no_exception_random_double(self, hash_function_1, hash_function_2):
        """tests randomization"""
        hash_2_args = hash_function_2()
        hash_2_args[0] = hash_2_args[0] + "2"
        with mock.patch(
            "sys.argv",
            random_argument("doublehashing") + hash_function_1() + hash_2_args,
        ):
            try:
                with pytest.raises(SystemExit) as pytest_exit:
                    pyAlgoTask.main()
                    sys.exit(0)
                task = task_base.get_task_by_cmd("hashing", "doublehashing")
                assert pytest_exit.value.code == 0, (
                    f"The argument {sys.argv} on input {task.task_io.randomizer.last_result} "
                    f"exited with error code but should not have."
                )
            except BaseException as exc:  # pylint: disable=broad-exception-caught
                task = task_base.get_task_by_cmd("hashing", "doublehashing")
                assert False, (
                    f"The argument {sys.argv} on input {task.task_io.randomizer.last_result} "
                    f"raised the exception '{exc}' but should not have."
                )
