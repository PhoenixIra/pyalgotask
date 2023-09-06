"""Module for insertion sort task"""
from ... import language as lang
from .. import task_base
from .sorting_base import Sorting


class Insertion(Sorting):
    """Insertion sort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 19

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort"""

    def __init__(self):
        """Constructor initialized cmd and exercise texts infos"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="insertion",
            description="Exercise to apply insertion sort on an unsorted array.",
            help="Insertion sort on array of integers.",
        )
        self.exercise_texts[0] = lang.get_text("sorting", "insertion-prefix")
        self.exercise_texts[1] = lang.get_text("sorting", "insertion-postfix")

    def init_sorting_argument_parser(self, parser):
        """No additional parseres required

        :param parser: argparser parser"""

    def sorting_parse(self, arg_input) -> None:
        """No additional parsers required

        :param arg_input: result of argparser"""

    def algorithm(self):
        """Insertion sort yielding after every insertion

        :yield: the array after every insertion"""
        array = self.array.copy()
        length = len(array)

        for i in range(1, length):
            key = array[i]
            j = i - 1
            while j >= 0 and array[j] > key:
                array[j + 1] = array[j]
                j = j - 1
            array[j + 1] = key
            yield (array.copy(), None)


task_base.register_task("sorting", Insertion())
