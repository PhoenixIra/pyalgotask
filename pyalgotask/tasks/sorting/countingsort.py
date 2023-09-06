"""Module for counting sort task"""

from ... import language as lang
from ...output.array import ArrayOutput
from ...randomizer.array import RandomIntArray
from ...tasks import task_base

from .sorting_base import Sorting


class Countingsort(Sorting):
    """Counting sort as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 209

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort"""

    def __init__(self):
        """Constructor initialized cmd and exercise texts infos"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="counting",
            description="Exercise to apply counting sort on an unsorted array.",
            help="Counting sort on array of integers.",
        )
        self.exercise_texts[0] = lang.get_text("sorting", "counting-prefix")
        self.exercise_texts[1] = lang.get_text("sorting", "counting-postfix")
        self.task_io.randomizer = RandomIntArray(0, 9)

    def init_sorting_argument_parser(self, parser):
        """No additional parseres required

        :param parser: argparser parser"""

    def sorting_parse(self, arg_input) -> None:
        """Checks that the input is non-negative

        :param arg_input: result from argparse"""
        self.task_io.output = ArrayOutput(
            self.array, self.exercise_texts[0], self.exercise_texts[1], self.algorithm
        )
        max_int = max(self.array) + 1
        length = len(self.array)
        self.task_io.output.init_exercise_output(
            lengths_of_arrays=[max_int, max_int, length],
            phantom_length=len(str(max_int)),
            left_labels=["C:", "C:", "B:"],
        )

    def algorithm(self):
        """Countingsort that yields after the fillings of the (help) arrays

        :yield: after the c array is initialized, fully created and
            after the b array is fully created
        """
        array = self.array.copy()
        length = len(array)
        max_int = max(array)
        array_b = [0] * length
        array_c = [0] * (max_int + 1)

        for j in range(0, length):
            array_c[array[j]] = array_c[array[j]] + 1

        yield (array_c.copy(), None)

        for i in range(1, max_int + 1):
            array_c[i] = array_c[i] + array_c[i - 1]

        yield (array_c.copy(), None)

        for j in reversed(range(0, length)):
            array_b[array_c[array[j]] - 1] = array[j]
            array_c[array[j]] = array_c[array[j]] - 1

        yield (array_b.copy(), None)


task_base.register_task("sorting", Countingsort())
