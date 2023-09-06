"""Module for merge sort task"""
import math

from .. import task_base
from ... import language as lang

from .sorting_base import Sorting


def _merge(array, left_index, middle_index, right_index):
    """Merge for mergesort

    :param array: array to apply merge on
    :param left_index: the left bound
    :param middle_index: the middle bound
    :param right_index: the right bound"""
    length_left = middle_index - left_index + 1  # length of A[p:q]
    length_right = right_index - middle_index  # length of A[q+1:r]
    array_left = [0] * length_left
    array_right = [0] * length_right

    for i in range(0, length_left):
        array_left[i] = array[left_index + i]
    for j in range(0, length_right):
        array_right[j] = array[middle_index + j + 1]

    i, j, k = 0, 0, left_index

    while i < length_left and j < length_right:
        if array_left[i] <= array_right[j]:
            array[k] = array_left[i]
            i += 1
        else:
            array[k] = array_right[j]
            j += 1
        k += 1

    while i < length_left:
        array[k] = array_left[i]
        i += 1
        k += 1
    while j < length_right:
        array[k] = array_right[j]
        j += 1
        k += 1


def _mergesort(array, left_index, right_index):
    """Mergesort yielding after every merge

    :param array: array to apply merge sort on
    :param left_index: the left index to sort
    :param right_index: the right index to sort

    :yield: array after every merge"""
    if left_index >= right_index:
        return
    middle_index = math.floor((left_index + right_index) / 2)
    yield from _mergesort(array, left_index, middle_index)
    yield from _mergesort(array, middle_index + 1, right_index)
    _merge(array, left_index, middle_index, right_index)
    highlight = (
        ([False] * left_index)
        + ([True] * (right_index - left_index + 1))
        + ([False] * (len(array) - right_index))
    )
    yield (array.copy(), highlight)


class Merge(Sorting):
    """Merge sort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 36-39

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort"""

    def __init__(self):
        """Constructor initialized cmd and exercise texts infos"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="merge",
            description="Exercise to apply merge sort on an unsorted array.",
            help="Merge sort on array of integers.",
        )
        self.exercise_texts[0] = lang.get_text("sorting", "merge-prefix")
        self.exercise_texts[1] = lang.get_text("sorting", "merge-postfix")

    def init_sorting_argument_parser(self, parser):
        """No additional parseres required

        :param parser: argparser parser"""

    def sorting_parse(self, arg_input) -> None:
        """No additional parsers required

        :param arg_input: result of argparser"""

    def algorithm(self):
        """Mergesort yielding after every merge

        :yield: array after merge"""
        array = self.array.copy()
        length = len(array)

        yield from _mergesort(array, 0, length - 1)


task_base.register_task("sorting", Merge())
