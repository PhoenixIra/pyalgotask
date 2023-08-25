"""Module for selection sort task"""
import pyalgotask.language as lang
from pyalgotask.tasks import task_base
from .sorting_base import Sorting


class Selection(Sorting):
    """Selection sort as in Knuth.
    The Art of Computer Programming 2ed. 1998. Addison-Wesley, page 139

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort"""

    def __init__(self):
        """Constructor initialized cmd and exercise texts infos"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="selection",
            description="Exercise to apply selection sort on an unsorted array.",
            help="Selection sort on array of integers.",
        )
        self.exercise_texts[0] = lang.get_text("sorting", "selection-prefix")
        self.exercise_texts[1] = lang.get_text("sorting", "selection-postfix")

    def init_sorting_argument_parser(self, parser):
        """No additional parseres required

        :param parser: argparser parser"""

    def sorting_parse(self, arg_input) -> None:
        """No additional parsers required

        :param arg_input: result of argparser"""

    def algorithm(self):
        """Selection sort yielding after every swap

        :yield: array after each swap"""
        array = self.array.copy()
        length = len(array)

        for j in reversed(range(0, length)):
            max_value = 0
            for i in range(1, j + 1):
                if array[max_value] <= array[i]:
                    max_value = i
            array[j], array[max_value] = array[max_value], array[j]
            yield (array.copy(), None)


task_base.register_task("sorting", Selection())
