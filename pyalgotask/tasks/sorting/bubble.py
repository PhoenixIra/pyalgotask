"""Module for bubble sort task"""
from ... import language as lang

from .. import task_base
from .sorting_base import Sorting


class Bubble(Sorting):
    """Bubble sort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 46

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort"""

    def __init__(self):
        """Constructor initialized cmd and exercise texts infos"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="bubble",
            description="Exercise to apply bubble sort on an unsorted array.",
            help="Bubble sort on array of integers.",
        )
        self.exercise_texts[0] = lang.get_text("sorting", "bubble-prefix")
        self.exercise_texts[1] = lang.get_text("sorting", "bubble-postfix")

    def init_sorting_argument_parser(self, parser):
        """No additional parseres required

        :param parser: argparser parser"""

    def sorting_parse(self, arg_input) -> None:
        """No additional parsers required

        :param arg_input: result of argparser"""

    def algorithm(self):
        """Classic Bubblesort going from right to left

        :yield: one step after each swap"""
        array = self.array.copy()
        length = len(array)

        for i in range(0, length - 1):
            for j in reversed(range(i + 1, length)):
                if array[j] < array[j - 1]:
                    array[j], array[j - 1] = array[j - 1], array[j]
                    yield (array.copy(), None)


task_base.register_task("sorting", Bubble())
