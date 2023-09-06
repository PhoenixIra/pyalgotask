"""Module for heap sort tasks"""
import math

from ... import language as lang
from .. import task_base

from .sorting_base import Sorting


def _parent(index):
    """
    The parent node in a heap of index i

    :param index: the index
    :return: parent index of index"""
    return math.floor((index + 1) / 2) - 1


def _left(index):
    """
    The left node in a heap of index i

    :param index: the index
    :return: left index of index"""
    return 2 * (index + 1) - 1


def _right(index):
    """
    The right node in a heap of index i

    :param index: the index
    :return: right index of index"""
    return 2 * (index + 1)


def _max_heapify(array, index, length):
    """Makes array to a max heap starting with index

    :param array: the heap
    :param index: start index"""
    largest = index
    while True:
        index = largest

        left = _left(index)
        right = _right(index)

        if left < length and array[left] > array[index]:
            largest = left
        if right < length and array[right] > array[largest]:
            largest = right

        if largest == index:
            break

        array[index], array[largest] = array[largest], array[index]


def _build_max_heap(array):
    """Translation from 1 indexed (size m) to 0 indexes (size n):
    floor(m/2) = floor(n/2)-1
    Thus, if we want to start at this, we reverse range till floor(n/2).

    :param array: the array for which a heap is created
    """
    length = len(array)
    first_leaf = math.floor(length / 2)
    for i in reversed(range(0, first_leaf)):
        _max_heapify(array, i, length)


class Heapsort(Sorting):
    """heap sort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 161-172

    max_heapify is implemented in non-recusive style. Morever, the array here starts at 0 not 1.

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort"""

    def __init__(self):
        """Constructor initialized cmd and exercise texts infos"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="heap",
            description="Exercise to apply heap sort on an unsorted array.",
            help="Heap sort on array of integers.",
        )
        self.exercise_texts[0] = lang.get_text("sorting", "heap-prefix")
        self.exercise_texts[1] = lang.get_text("sorting", "heap-postfix")

    def init_sorting_argument_parser(self, parser):
        """No additional parseres required

        :param parser: argparser parser"""

    def sorting_parse(self, arg_input) -> None:
        """No additional parsers required

        :param arg_input: result of argparser"""

    def algorithm(self):
        """Heapsort yielding after building max heap and every get highest operation

        :yield: array after build max heap and after every heapify, highlights the sorted part
        """
        array = self.array.copy()
        length = len(array)

        _build_max_heap(array)
        yield (array, None)
        for i in reversed(range(1, length)):
            array[0], array[i] = array[i], array[0]
            length -= 1
            _max_heapify(array, 0, i)
            highlight = [False] * length + [True] * (len(array) - length)
            yield (array, highlight)


task_base.register_task("sorting", Heapsort())
