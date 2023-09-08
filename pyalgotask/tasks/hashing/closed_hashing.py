"""Module containing various hash table methods using probing"""
from abc import abstractmethod
from enum import Enum, auto
import math

from pyalgotask.structures.operation import OperationType
from pyalgotask.randomizer.parameter import FloatParameterRandomizer
from pyalgotask import language as lang

from pyalgotask.tasks import task_base
from pyalgotask.tasks.hashing import hashing_base


class _SpecialValue(Enum):
    NIL = auto()
    DELETED = auto()

    def __repr__(self):
        if self == _SpecialValue.NIL:
            return ""
        if self == _SpecialValue.DELETED:
            return "DEL"
        raise NotImplementedError(f"{self} is not yet implemented!")

    def __str__(self):
        return self.__repr__()


class ProbingHashing(hashing_base.Hashing):
    """Closed Hashing as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 294

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar hashtable_size: the size of the hash table to use
    :ivar hash_function: the (first) hash function to use
    :ivar exercise_texts: prefix and postfix of the task description
    :ivar operations: the operation to apply to the hash table
    """

    @abstractmethod
    def parse_closed_hashing(self, arg_input):
        """Method for parsing values from argparse that are specific
        to certain closed hashing methods

        :param arg_input: the output of argparse"""

    def parse_hashing(self, arg_input):
        """Parse function for arguments which are hashing method specific

        :param arg_input: the result from argparser"""

        labels = [[f"a[{i}]" for i in range(0, self.hashtable_size)]]

        self.task_io.output.init_exercise_output(
            lengths_of_arrays=[self.hashtable_size], top_labels=labels
        )

        self.parse_closed_hashing(arg_input)

    @abstractmethod
    def probing(self, value, index):
        """Probing method for the hashtable method

        :param value: the value to hash
        :param index: the current probing index
        :return: a hash value for value and index"""

    def algorithm(self):
        """The base algorithm using probing on insert and delete operations

        :yield: the result after all steps as intermediate steps are usually to fine"""
        hashtable = [_SpecialValue.NIL for _ in range(self.hashtable_size)]

        for operation in self.operations:
            if operation.is_operation_type(OperationType.INSERT):
                if not self.insert(hashtable, operation.value):
                    raise ValueError("Hashtable not suffiently big for operations.")
            elif operation.is_operation_type(OperationType.DELETE):
                if not self.delete(hashtable, operation.value):
                    raise ValueError(f"Operation {operation} did not suceed!")
            else:
                raise NotImplementedError(
                    f"Operator {operation.type} not supported by task {self.__class__.__name__}"
                )

        yield ((hashtable, None))

    def insert(self, hashtable, value):
        """The base insert method for hashtables and probing

        :param hashtable: the hashtable to insert into'
        :param value: the value to insert into the hashtable"""
        for i in range(0, len(hashtable)):
            hash_value = self.probing(value, i)
            if (
                hashtable[hash_value] == _SpecialValue.NIL
                or hashtable[hash_value] == _SpecialValue.DELETED
            ):
                hashtable[hash_value] = value
                return True
        return False

    def delete(self, hashtable, value):
        """The base delete method for hashtables and probing

        :param hashtable: the hashtable to delete from'
        :param value: the value to delete from the hashtable"""
        for i in range(0, len(hashtable)):
            hash_value = self.probing(value, i)
            if hashtable[hash_value] == _SpecialValue.NIL:
                return False
            if hashtable[hash_value] == value:
                hashtable[hash_value] = _SpecialValue.DELETED
                return True
        return False


class LinearProbingHashing(ProbingHashing):
    """Closed Hashing as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 294

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar hashtable_size: the size of the hash table to use
    :ivar hash_function: the (first) hash function to use
    :ivar exercise_texts: prefix and postfix of the task description
    :ivar operations: the operation to apply to the hash table
    """

    def __init__(self):
        """Constructor to set cmd and exercise text"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="linearprobing",
            description=(
                "Exercise to apply closed hashing (i.e. with probing) "
                "on insert and delete operations into hashtables with linear probing."
            ),
            help="Linear closed hashing (i.e. probing) for operations on integers.",
        )
        self.exercise_texts[0] = lang.get_text("hashing", "probing-prefix")
        self.exercise_texts[1] = lang.get_text(
            "hashing", "probing-postfix"
        ) + lang.get_text("hashing", "probing-linear")

    def init_hashing_argument_parser(self, parser):
        """No additional parser arguments required

        :param parser: argparser object"""

    def parse_closed_hashing(self, arg_input):
        """No additional parser arguments required

        :param arg_input: argparser result"""

    def probing(self, value, index):
        """linear probing method

        :param value: the value to hash
        :param index: the current probing index
        :return: a hash value for value and index"""
        return (self.hash_function(value) + index) % self.hashtable_size


class QuadraticProbingHashing(ProbingHashing):
    """Closed Hashing as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 294

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar hashtable_size: the size of the hash table to use
    :ivar hash_function: the (first) hash function to use
    :ivar exercise_texts: prefix and postfix of the task description
    :ivar operations: the operation to apply to the hash table
    :ivar random_constant: additional randomizer for constants
    :ivar constant: constants used in quadratic hashing
    """

    def __init__(self):
        """Constructor to set cmd and exercise text"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="quadraticprobing",
            description=(
                "Exercise to apply closed hashing (i.e. with probing) "
                "on insert and delete operations into hashtables with linear probing."
            ),
            help="Quadratic closed hashing (i.e. probing) for operations on integers.",
        )
        self.exercise_texts[0] = lang.get_text("hashing", "probing-prefix")
        self.exercise_texts[1] = lang.get_text(
            "hashing", "probing-postfix"
        ) + lang.get_text("hashing", "probing-quadratic")

        self.random_constant = None
        self.constant = [None, None]

    def init_hashing_argument_parser(self, parser):
        """Sets the arguments for the constants in the probing mechanism

        :param parser: the argparser parser"""
        parser.add_argument(
            "--constants",
            type=float,
            dest="hashing_probing_constants",
            nargs=2,
            metavar=("LINEAR_CONST", "QUADRATIC_CONST"),
            help="Sets the constants for quadratic proving",
        )
        self.random_constant = FloatParameterRandomizer(parameter_name="constants")
        self.random_constant.init_argument_parser(parser)

    def parse_closed_hashing(self, arg_input):
        """Reads the arguments for the constants in this probing mechanism

        :param arg_input: the argparse result"""
        self.random_constant.parse(arg_input)
        if arg_input.hashing_probing_constants:
            self.constant[0] = arg_input.hashing_probing_constants[0]
            self.constant[1] = arg_input.hashing_probing_constants[1]
        else:
            self.constant[0] = self.random_constant.get_random_input()
            self.constant[1] = self.random_constant.get_random_input()

    def probing(self, value, index):
        """quadratic probing method

        :param value: the value to hash
        :param index: the current probing index
        :return: a hash value for value and index"""
        return (
            math.floor(
                self.hash_function(value)
                + self.constant[0] * index
                + self.constant[1] * index * index
            )
            % self.hashtable_size
        )


class DoubleProbingHashing(ProbingHashing):
    """Closed Hashing as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 294

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar hashtable_size: the size of the hash table to use
    :ivar hash_function: the first hash function to use
    :ivar hash_function_2: the second hash function to use
    :ivar exercise_texts: prefix and postfix of the task description
    :ivar operations: the operation to apply to the hash table
    """

    def __init__(self):
        """Constructor to set cmd and exercise text"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="doublehashing",
            description=(
                "Exercise to apply closed hashing (i.e. with probing) "
                "on insert and delete operations into hashtables with double hashing."
            ),
            help="Double closed hashing (i.e. probing) for operations on integers.",
        )
        self.exercise_texts[0] = lang.get_text("hashing", "probing-prefix")
        self.exercise_texts[1] = lang.get_text("hashing", "probing-double-postfix")

        self.hash_function_2 = None

    def init_hashing_argument_parser(self, parser):
        """Sets the arguments for the constants in the probing mechanism

        :param parser: the argparser parser"""
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "--div2",
            type=int,
            dest="hash2_div",
            help="Selects the devision method as second hash-function",
        )
        group.add_argument(
            "--mult2",
            type=float,
            dest="hash2_mult",
            nargs=2,
            help=(
                "Selects the multiplication method as second hash-function "
                "with a constant and a size constant"
            ),
        )
        group.add_argument(
            "--mult-shift2",
            type=int,
            dest="hash2_shift",
            nargs=2,
            help=(
                "Selects the multiply-shift method as hash-function "
                "with the constant and the exponent of 2"
            ),
        )

    def parse_closed_hashing(self, arg_input):
        """Nothing left to parse here

        :param arg_input: the argparse result"""

    def parse_hash_function(self, arg_input):
        """Reads the arguments for the constants in this probing mechanism

        :param arg_input: the argparse result"""
        self.parse_first_hash_function(arg_input)
        self.parse_second_hash_function(arg_input)

    def parse_first_hash_function(self, arg_input):
        """Reads the arguments for the constants for the first hash_function

        :param arg_input: the argparse result"""
        if arg_input.hash_div:
            self.hashtable_size = arg_input.hash_div
            self.hash_function = hashing_base.division_hashing(self.hashtable_size)
            self.exercise_texts[0] = self.exercise_texts[0].format(self.hashtable_size)
            self.exercise_texts[1] += lang.get_text(
                "hashing", "division-doublehash-function"
            ).format(1, self.hashtable_size)

        elif arg_input.hash_mult:
            self.hashtable_size = int(arg_input.hash_mult[1])
            multiplication_constant = arg_input.hash_mult[0]
            if not 0 < multiplication_constant < 1:
                raise ValueError(
                    (
                        "Multiplication Constant is not properly set, "
                        f"needs to be between in (0,1) but is {multiplication_constant}"
                    )
                )
            self.hash_function = hashing_base.mutlitpilcation_hashing(
                multiplication_constant, self.hashtable_size
            )
            self.exercise_texts[0] = self.exercise_texts[0].format(self.hashtable_size)
            self.exercise_texts[1] += lang.get_text(
                "hashing", "multiplication-doublehash-function"
            ).format(1, multiplication_constant, self.hashtable_size)

        elif arg_input.hash_shift:
            shift_constant = arg_input.hash_shift[1]
            self.hashtable_size = 2**shift_constant
            if not 0 < shift_constant <= hashing_base.get_int_bits():
                raise ValueError(
                    (
                        "Shift Constant is not properly set, "
                        f"needs to be an integer in (0,{hashing_base.get_int_bits()}] "
                        f"but is {shift_constant}"
                    )
                )
            multiplication_constant = arg_input.hash_shift[0]
            if not 0 < multiplication_constant <= 2 ** hashing_base.get_int_bits():
                raise ValueError(
                    (
                        "Multiply-Shift Constant is not properly set, "
                        f"needs to be an integer in (0,2**{hashing_base.get_int_bits()}] "
                        f"but is {multiplication_constant}"
                    )
                )
            self.hash_function = hashing_base.multiply_shift_hashing(
                multiplication_constant, shift_constant
            )
            self.exercise_texts[0] = self.exercise_texts[0].format(self.hashtable_size)
            self.exercise_texts[1] += lang.get_text(
                "hashing", "multiply-shift-doublehash-function"
            ).format(
                1,
                multiplication_constant,
                hashing_base.get_int_bits(),
                shift_constant,
            )

        else:
            raise ValueError("No first hash function selected!")

    def parse_second_hash_function(self, arg_input):
        """Reads the arguments for the constants for the second hash_function

        :param arg_input: the argparse result"""
        if arg_input.hash2_div:
            size_constant = arg_input.hash2_div
            self.hash_function_2 = hashing_base.division_hashing(size_constant)
            self.exercise_texts[1] += " " + lang.get_text(
                "hashing", "division-doublehash-function"
            ).format(2, size_constant)

        elif arg_input.hash2_mult:
            size_constant = int(arg_input.hash2_mult[1])
            multiplication_constant = arg_input.hash2_mult[0]
            if not 0 < multiplication_constant < 1:
                raise ValueError(
                    (
                        "Multiplication Constant is not properly set, "
                        f"needs to be between in (0,1) but is {multiplication_constant}"
                    )
                )
            self.hash_function_2 = hashing_base.mutlitpilcation_hashing(
                multiplication_constant, size_constant
            )
            self.exercise_texts[0] += " " + lang.get_text(
                "hashing", "multiplication-doublehash-function"
            ).format(2, multiplication_constant, size_constant)

        elif arg_input.hash2_shift:
            shift_constant = arg_input.hash2_shift[1]
            size_constant = 2**shift_constant
            if not 0 < shift_constant <= hashing_base.get_int_bits():
                raise ValueError(
                    (
                        "Shift Constant is not properly set, "
                        f"needs to be an integer in (0,{hashing_base.get_int_bits()}] "
                        f"but is {shift_constant}"
                    )
                )
            multiplication_constant = arg_input.hash2_shift[0]
            if not 0 < multiplication_constant <= 2 ** hashing_base.get_int_bits():
                raise ValueError(
                    (
                        "Multiply-Shift Constant is not properly set, "
                        f"needs to be an integer in (0,2**{hashing_base.get_int_bits()}] "
                        f"but is {multiplication_constant}"
                    )
                )
            self.hash_function_2 = hashing_base.multiply_shift_hashing(
                multiplication_constant, shift_constant
            )
            self.exercise_texts[1] += " " + lang.get_text(
                "hashing", "multiply-shift-doublehash-function"
            ).format(
                2, multiplication_constant, hashing_base.get_int_bits(), shift_constant
            )

        else:
            raise ValueError("No second hash function selected!")

    def probing(self, value, index):
        """Probing mechanism using double hashing

        :param value: the value to hash
        :param index: the current probing index
        :return: (h1(value) + h2(index)) modulo hashtable_size"""
        return (
            self.hash_function(value) + self.hash_function_2(index)
        ) % self.hashtable_size


task_base.register_task("hashing", LinearProbingHashing())
task_base.register_task("hashing", QuadraticProbingHashing())
task_base.register_task("hashing", DoubleProbingHashing())
