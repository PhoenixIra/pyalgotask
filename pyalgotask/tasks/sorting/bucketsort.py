"""Module for bucket sort task"""
import math

from ... import language as lang

from .. import task_base
from ...output.array import ArrayOutput
from ...randomizer.array import RandomFloatArray
from .sorting_base import Sorting


def str_to_zero_one(value: str) -> float:
    """cast method to check whether the float is 0 1 bounded"""
    i = float(value)
    if i < 0:
        raise ValueError(f"Only floats in [0,1) allowed, but {value} is negative")
    if i >= 1:
        raise ValueError(f"Only floats in [0,1) allowed, but {value} is 1 or above")
    return i


def _insertion_sort(array):
    """Insertion sort for helping with bucketsort

    :param array: the array to sort"""
    length = len(array)

    for i in range(1, length):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j = j - 1
        array[j + 1] = key


class Bucketsort(Sorting):
    """Bucket sort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 213

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort"""

    def __init__(self):
        """Constructor initialized cmd and exercise texts infos"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="bucket",
            description="Exercise to apply bucket sort on an unsorted array in decimal system.",
            help="Bucket sort on array of decimal integers.",
        )
        self.exercise_texts[0] = lang.get_text("sorting", "bucket-prefix")
        self.exercise_texts[1] = lang.get_text("sorting", "bucket-postfix")
        self.task_io.parser.cast_function = str_to_zero_one
        self.task_io.randomizer = RandomFloatArray()

    def init_sorting_argument_parser(self, parser):
        """No additional parseres required

        :param parser: argparser parser"""

    def sorting_parse(self, arg_input):
        """Checks that the input is actually correct floats

        :param arg_input: result from argparse"""
        self.task_io.output = ArrayOutput(
            self.array, self.exercise_texts[0], self.exercise_texts[1], self.algorithm
        )
        if (
            self.task_io.randomizer.min_value < 0
            or self.task_io.randomizer.max_value > 1
        ):
            raise ValueError(
                (
                    "Selected to big range "
                    f"[{self.task_io.randomizer.min_value},{self.task_io.randomizer.max_value}] "
                    "for randomized values."
                )
            )
        max_str_length = max(len(str(x)) for x in self.array)
        length = len(self.array)
        self.task_io.output.init_exercise_output(
            lengths_of_arrays=[len(self.array)] * (length + 1),
            phantom_length=max_str_length,
            left_labels=[
                f"[{i / length:.2f},{(i + 1) / length:.2f}):" for i in range(0, length)
            ]
            + ["A:"],
        )

    def algorithm(self):
        """Bucketsort yielding the sorted buckets and the sorted list

        :yield: the sorted buckets"""
        array = self.array.copy()
        length = len(array)

        array_b = [[] for _ in range(length)]

        for i in range(0, length):
            array_b[math.floor(length * array[i])].append(array[i])

        for i in range(0, length):
            _insertion_sort(array_b[i])

        for j in range(0, length):
            yield (array_b[j].copy(), None)

        array = [x for sublist in array_b for x in sublist]
        yield (array.copy(), None)


task_base.register_task("sorting", Bucketsort())
