"""Module for radix sort task"""
import math

from pyalgotask.tasks import task_base
from pyalgotask import language as lang

from pyalgotask.tasks.sorting.sorting_base import Sorting


def str_to_nat(value: str) -> int:
    """Function to cast strings to natural number"""
    i = int(value)
    if i < 0:
        raise ValueError(f"Only natural numbers are allowed, but {value} is negative")
    return i


def _digit(value, position):
    """Calculates the digit at position in base 10

    :param value: value for which the digit is calculated
    :param position: position of the digit
    :return: the digit of value at position"""
    return math.floor(value / 10**position) % 10


def _stable_sort(array, position, max_value):
    """An easy stable sort sorting in linear time when elements are finite
    by copying all values in a new array

    :param array: array to sort
    :param position: digit position to sort
    :param max_value: the max_value any digit can have
    :return: array sorted according to position"""
    array_b = [0] * len(array)

    index_b = 0
    for digit in range(max_value + 1):
        for value in array:
            if _digit(value, position) == digit:
                array_b[index_b] = value
                index_b += 1
    return array_b


class Radixsort(Sorting):
    """Radix sort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 213

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort
    """

    def __init__(self):
        """Constructor initialized cmd and exercise texts infos"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="radix",
            description="Exercise to apply radix sort on an unsorted array in decimal system.",
            help="Radix sort on array of decimal integers.",
        )
        self.exercise_texts[0] = lang.get_text("sorting", "radix-prefix")
        self.exercise_texts[1] = lang.get_text("sorting", "radix-postfix")
        self.task_io.parser.cast_function = str_to_nat

    def init_sorting_argument_parser(self, parser):
        """No additional parseres required

        :param parser: argparser parser"""

    def sorting_parse(self, arg_input) -> None:
        """No additional parsers required

        :param arg_input: result of argparser"""

    def algorithm(self):
        """Radixsort yielding after every sorted digit

        :yield: array after ever sorted digit"""
        array = self.array.copy()
        max_value = max(array)

        num_of_digits = math.ceil(math.log(max_value, 10))

        for i in range(num_of_digits):
            array = _stable_sort(array, i, max_value)
            yield (array.copy(), None)


task_base.register_task("sorting", Radixsort())
