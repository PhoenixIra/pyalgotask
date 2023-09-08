"""Modul for the hashing category and its base class"""

from abc import abstractmethod
import math

from pyalgotask.tasks import task_base
from pyalgotask.output.array import OperationsArrayOutput
from pyalgotask.input.in_del_operators import InDelOperators
from pyalgotask.randomizer.in_del_operators import RandomInDelOperations
from pyalgotask import language as lang


def division_hashing(size_constant):
    """generates a hashing method with fixed size_constant

    :param size_constant: the size of the hashtable"""

    def hash_method(value):
        """hash function using the devision method

        :param value: value to hash
        :return: value modulo size_constant"""
        return value % size_constant

    return hash_method


def mutlitpilcation_hashing(multiplication_constant, size_constant):
    """generates a mutliplication method hash function

    :param size_constant: the hashtable size
    :param multiplication_constant: the constant for multiplication with"""

    def hash_method(value):
        """hash function using the multiplication method

        :param value: value to hash
        :return: (value * constant) modulo 1 * size_constant"""
        return math.floor(((value * multiplication_constant) % 1) * size_constant)

    return hash_method


_INT_BITS = 4


def get_int_bits():
    """
    for reading the number of bits used in the multiply shift hashing method

    :return: 4
    """
    return _INT_BITS


def multiply_shift_hashing(multiplication_constant, shift_constant):
    """generates a multipliy Shift method hash function

    :param shift_constant: the hashtable size in logarithm
    :param multiplication_constant: the constant for multiplication with"""

    def hash_method(value):
        """hash function using the multiplication method

        :param value: value to hash
        :return: ((value * multiplication_constant) modulo 2^(integer bits)) \
            left shift (integer bits) - shift_constant
        """
        return ((value * multiplication_constant) % 2**_INT_BITS) >> (
            _INT_BITS - shift_constant
        )

    return hash_method


class Hashing(task_base.Task):
    """
    Hashing functions as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 284-285

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar hashtable_size: the size of the hash table to use
    :ivar hash_function: the (first) hash function to use
    :ivar exercise_texts: prefix and postfix of the task description
    :ivar operations: the operation to apply to the hash table
    """

    def __init__(self):
        """Constructor that initialized parser and randomizer"""
        super().__init__()
        self.task_io = task_base.TaskIO(
            parser=InDelOperators(),
            randomizer=RandomInDelOperations(),
            output=None,
            randomized=False,
        )

        self.hashtable_size = None
        self.hash_function = None
        self.exercise_texts = [None, None]
        self.operations = None

    @abstractmethod
    def init_hashing_argument_parser(self, parser):
        """Method for hashing method specific argument initialization

        :param parser: the argparse parser"""

    def init_argument_parser(self, parser):
        """Initialized the arguments for the parser and for sort specific.

        :param parser: the argparse parser"""
        self.task_io.parser.init_argument_parser(parser)
        self.task_io.randomizer.init_argument_parser(parser)
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "--div",
            type=int,
            dest="hash_div",
            metavar="SIZE",
            help=(
                "Selects the devision method as hash-function "
                "with the respective hash table size"
            ),
        )
        group.add_argument(
            "--mult",
            type=float,
            dest="hash_mult",
            nargs=2,
            metavar=("CONSTANT", "SIZE"),
            help=(
                "Selects the multiplication method as hash-function "
                "with a constant and the respective hash table size"
            ),
        )
        group.add_argument(
            "--mult-shift",
            type=int,
            dest="hash_shift",
            nargs=2,
            metavar=("CONSTANT", "LOG_SIZE"),
            help=(
                "Selects the multiply-shift method as hash-function "
                "with the constant and the exponent of 2 as the hash table size"
            ),
        )
        self.init_hashing_argument_parser(parser)

    @abstractmethod
    def parse_hashing(self, arg_input):
        """Parse function for arguments which are hashing method specific

        :param arg_input: the result from argparser"""

    def parse_hash_function(self, arg_input):
        """Parse function for parsing the hash function

        :param arg_input: the result from argparser"""
        if arg_input.hash_div:
            self.hashtable_size = arg_input.hash_div
            self.hash_function = division_hashing(self.hashtable_size)
            self.exercise_texts[0] = self.exercise_texts[0].format(self.hashtable_size)
            self.exercise_texts[1] += lang.get_text(
                "hashing", "division-hash-function"
            ).format(self.hashtable_size)

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
            self.hash_function = mutlitpilcation_hashing(
                multiplication_constant, self.hashtable_size
            )
            self.exercise_texts[0] = self.exercise_texts[0].format(self.hashtable_size)
            self.exercise_texts[1] += lang.get_text(
                "hashing", "multiplication-hash-function"
            ).format(multiplication_constant, self.hashtable_size)

        elif arg_input.hash_shift:
            shift_constant = arg_input.hash_shift[1]
            self.hashtable_size = 2**shift_constant
            if not 0 < shift_constant <= _INT_BITS:
                raise ValueError(
                    (
                        "Shift Constant is not properly set, "
                        f"needs to be an integer in (0,{_INT_BITS}] but is {shift_constant}"
                    )
                )
            multiplication_constant = arg_input.hash_shift[0]
            if not 0 < multiplication_constant <= 2**_INT_BITS:
                raise ValueError(
                    (
                        "Multiply-Shift Constant is not properly set, "
                        f"needs to be an integer in (0,2**{_INT_BITS}] "
                        f"but is {multiplication_constant}"
                    )
                )
            self.hash_function = multiply_shift_hashing(
                multiplication_constant, shift_constant
            )
            self.exercise_texts[0] = self.exercise_texts[0].format(self.hashtable_size)
            self.exercise_texts[1] += lang.get_text(
                "hashing", "multiply-shift-hash-function"
            ).format(multiplication_constant, _INT_BITS, shift_constant)

        else:
            raise ValueError("No hash function selected!")

    def parse(self, arg_input) -> None:
        """Parse function to call lower parse functions and
        to initialize output and operations classes

        :param arg_input: the result from argparser"""
        self.task_io.parser.parse(arg_input)
        self.task_io.randomizer.parse(arg_input)
        if self.task_io.parser.data:
            self.operations = self.task_io.parser.data
        else:
            self.task_io.randomized = True
            self.operations = self.task_io.randomizer.get_random_input()

        self.parse_hash_function(arg_input)

        self.task_io.output = OperationsArrayOutput(
            self.operations,
            self.exercise_texts[0],
            self.exercise_texts[1],
            self.algorithm,
        )

        self.parse_hashing(arg_input)

    def generate_preamble(self):
        """Method to generate an preamble latex code for this task

        :return: the preamble of this task"""
        return self.task_io.output.latex_options.preamble

    def generate_exercise(self):
        """Method to generate an exercise LaTeX file code

        :return: the ``LatexObject`` representing the exercise"""
        return self.task_io.output.generate_exercise()

    def generate_solution(self):
        """Method to generate an solution LaTeX file code

        :return: the ``LatexObject`` representing the solution"""
        return self.task_io.output.generate_solution()


task_base.register_category(
    "hashing",
    "Hashtables with hash functions",
    "Various hashtable data structures with various hash functions",
)
