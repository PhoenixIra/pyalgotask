"""Module for quick sort tasks"""
from ... import language as lang
from .. import task_base

from .sorting_base import Sorting


def _quicksort(array, left_index, right_index, partition_scheme):
    """Quicksort yielding after ever partition

    :param array: the array to sort
    :param left_index: left index to sort
    :param right_index: right_index to sort
    :param partition_scheme: the partition scheme to be used
    :yield: array after every partition with highlight on the sorted parted"""
    length = len(array)
    if left_index < right_index:
        pivot_index = partition_scheme(array, left_index, right_index)
        highlight = (
            [False] * left_index
            + [True] * (right_index - left_index + 1)
            + [False] * (length - right_index - 1)
        )
        yield (array.copy(), highlight)

        yield from _quicksort(array, left_index, pivot_index - 1, partition_scheme)
        yield from _quicksort(array, pivot_index + 1, right_index, partition_scheme)


class Quicksort(Sorting):
    """Quicksort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 183-184

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort
    :ivar partition_scheme: the partition scheme to use"""

    def __init__(self):
        """Constructor initialized cmd and exercise texts infos"""
        super().__init__()
        self.cmd_info = None
        self.exercise_texts[0] = lang.get_text("sorting", "quick-prefix")
        self.exercise_texts[1] = lang.get_text("sorting", "quick-postfix")
        self.partition_scheme = None

    def init_sorting_argument_parser(self, parser):
        """No additional parseres required

        :param parser: argparser parser"""

    def sorting_parse(self, arg_input) -> None:
        """No additional parsers required

        :param arg_input: result of argparser"""

    def algorithm(self):
        """Quicksort with genertic partition scheme that yields after every partition

        :yield: array after every partition"""
        array = self.array.copy()
        length = len(array)

        yield from _quicksort(array, 0, length - 1, self.partition_scheme)


def _partition_hoare(array, left_index, right_index):
    """Partitioning after Hoare using dual search

    :param array: array to sort
    :param left_index: left index to sort
    :param right_index: right index to sort"""
    right_value = array[right_index]
    i = left_index - 1
    j = right_index
    while True:
        j -= 1
        i += 1
        while array[j] > right_value:
            j -= 1
        while array[i] < right_value:
            i += 1

        if i < j:
            array[i], array[j] = array[j], array[i]
        else:
            array[i], array[right_index] = array[right_index], array[i]
            return i


class QuicksortHoare(Quicksort):
    """Quicksort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 183-184
    with the Hoare-Partition from page 199

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort
    :ivar partition_scheme: the Hoare partition scheme"""

    def __init__(self):
        """Constructor initialized cmd and the partition scheme"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="quick-hoare",
            description=(
                "Exercise to apply quicksort "
                "on an unsorted array with Hoares partition scheme."
            ),
            help="Quicksort on array of integers with Hoares partition.",
        )
        self.partition_scheme = _partition_hoare


def _partition_lomuto(array, left_index, right_index):
    """Partitioning after Lomuto using single search

    :param array: array to sort
    :param left_index: left index to sort
    :param right_index: right index to sort"""
    right_value = array[right_index]
    i = left_index - 1
    for j in range(left_index, right_index):
        if array[j] <= right_value:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[right_index] = array[right_index], array[i + 1]
    return i + 1


class QuicksortLomuto(Quicksort):
    """Quicksort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 183-184
    with the Lomuto-Partition

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort
    :ivar partition_scheme: the Lomuto partition scheme"""

    def __init__(self):
        """Constructor initialized cmd and the partition scheme"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="quick-lomuto",
            description=(
                "Exercise to apply quicksort "
                "on an unsorted array using Lomuto's partition scheme."
            ),
            help="Quicksort on array of integers.",
        )
        self.partition_scheme = _partition_lomuto


task_base.register_task("sorting", QuicksortLomuto())
task_base.register_task("sorting", QuicksortHoare())
