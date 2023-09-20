"""Base class for algorithms inserting or deleting in trees"""
from abc import abstractmethod

from pyalgotask.tasks import task_base

from pyalgotask.input.in_del_operators import InDelOperators
from pyalgotask.randomizer.in_del_operators import RandomInDelOperations
from pyalgotask.output.tree import TreeOutput


class Tree(task_base.Task):
    """
    Base tree class handling the tree IO

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar exercise_texts: texts for the exercise explanation
    :ivar operation: operations to execute on the tree"""

    def __init__(self):
        super().__init__()
        self.task_io = task_base.TaskIO(
            parser=InDelOperators(),
            randomizer=RandomInDelOperations(),
            randomized=False,
            output=None,
        )
        self.exercise_texts = [None, None]
        self.operations = None

    @abstractmethod
    def init_tree_argument_parser(self, parser):
        """Method for sorting specific argument initialization

        :param parser: the argparse parser"""

    def init_argument_parser(self, parser):
        """Initialized the arguments for the parser and for sort specific."""
        self.task_io.parser.init_argument_parser(parser)
        self.task_io.randomizer.init_argument_parser(parser)
        self.init_tree_argument_parser(parser)

    @abstractmethod
    def tree_parse(self, arg_input) -> None:
        """Parses the arguments for the sorting specific things.

        :param arg_input: the result of argparser"""

    def parse(self, arg_input) -> None:
        """Parses the arguments for the parser and for the sorting exercise.
        Also create the output array and initialized it.

        :param arg_input: the result of argparser"""
        self.task_io.parser.parse(arg_input)
        self.task_io.randomizer.parse(arg_input)
        if self.task_io.parser.data is not None:
            self.operations = self.task_io.parser.data
        else:
            self.task_io.randomized = True
            self.operations = self.task_io.randomizer.get_random_input()
        self.task_io.output = TreeOutput(
            self.operations,
            self.exercise_texts[0],
            self.exercise_texts[1],
            self.algorithm,
        )
        self.tree_parse(arg_input)

    @abstractmethod
    def algorithm(self):
        """The algorithm for which this generator is generating exercises

        :yield: intermediate steps"""


task_base.register_category(
    "tree",
    "Various tree algorithms",
    "Various tasks involving for tree algorithms",
)
