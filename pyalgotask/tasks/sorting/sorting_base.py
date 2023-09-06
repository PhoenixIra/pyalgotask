"""Base class for algorithms sorting an array of usually integer values"""
from abc import abstractmethod

from .. import task_base

from ...input.array import ArrayInput
from ...randomizer.array import RandomIntArray
from ...output.array import AlgorithmArrayOutput


class Sorting(task_base.Task):
    """
    Base sorting class handling the array IO

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar array: the array to sort"""

    def __init__(self):
        super().__init__()
        self.task_io = task_base.TaskIO(
            parser=ArrayInput(),
            randomizer=RandomIntArray(),
            randomized=False,
            output=None,
        )
        self.exercise_texts = [None, None]
        self.array = None

    @abstractmethod
    def init_sorting_argument_parser(self, parser):
        """Method for sorting specific argument initialization

        :param parser: the argparse parser"""

    def init_argument_parser(self, parser):
        """Initialized the arguments for the parser and for sort specific.

        :param parser: the argparse parser"""
        parser.add_argument(
            "--num-add-lines",
            dest="num_add_lines",
            help="Number of additional array lines the solution space should generate.",
            type=int,
            default=0,
        )
        self.task_io.parser.init_argument_parser(parser)
        self.task_io.randomizer.init_argument_parser(parser)
        self.init_sorting_argument_parser(parser)

    @abstractmethod
    def sorting_parse(self, arg_input) -> None:
        """Parses the arguments for the sorting specific things.

        :param arg_input: the result of argparser"""

    def parse(self, arg_input) -> None:
        """Parses the arguments for the parser and for the sorting exercise.
        Also create the output array and initialized it.

        :param arg_input: the result of argparser"""
        self.task_io.parser.parse(arg_input)
        self.task_io.randomizer.parse(arg_input)
        if self.task_io.parser.data is not None:
            if len(self.task_io.parser.data) < 2:
                raise ValueError(
                    (
                        f"Input {self.task_io.parser.data} not long enough, "
                        "needs to have at least 2 elements!"
                    )
                )
            self.array = self.task_io.parser.data
        else:
            self.task_io.randomized = True
            self.array = self.task_io.randomizer.get_random_input()
        self.task_io.output = AlgorithmArrayOutput(
            self.array, self.exercise_texts[0], self.exercise_texts[1], self.algorithm
        )
        self.task_io.output.init_exercise_algorithm_output(
            num_of_additional_arrays=arg_input.num_add_lines
        )
        self.sorting_parse(arg_input)

    @abstractmethod
    def algorithm(self):
        """The algorithm for which this generator is generating exercises

        :yield: intermediate steps"""

    def generate_preamble(self):
        """Method to generate an preamble latex code for this task

        :return: LaTeX object of the preamble"""
        return self.task_io.output.latex_options.preamble

    def generate_exercise(self):
        """Method to generate an exercise LaTeX file code

        :return: LaTeX object of the exercise"""
        return self.task_io.output.generate_exercise()

    def generate_solution(self):
        """Method to generate an solution LaTeX file code

        :return: LaTeX object of the solution"""
        return self.task_io.output.generate_solution()


task_base.register_category(
    "sorting",
    "Various sorting algorithms",
    "Various tasks involving for sorting algorithms",
)
