"""Module containing the base class called Task and 
the functionality to allow tasks register themself to the main method"""
import dataclasses
from abc import ABC, abstractmethod
from pylatex.base_classes.latex_object import LatexObject

from pyalgotask.input.input_base import Input
from pyalgotask.randomizer.randomizer_base import Randomizer
from pyalgotask.output.output_base import Output


@dataclasses.dataclass
class TaskIO:
    """Dataclass to bundle IO related classes

    :ivar parser: the parser for argparse output
    :ivar randomizer: randomizer in case no arguments were given
    :ivar randomized: should be set true if the randomizer is used
    :ivar output: generates LaTeX code for the ask"""

    parser: Input
    randomizer: Randomizer
    output: Output
    randomized: bool


@dataclasses.dataclass
class TaskCmd:
    """Dataclass to bundle cmd related information

    :ivar cmd: the actual cmd to execute this task
    :ivar description: description of this task
    :ivar help: help text for this task"""

    cmd: str
    description: str
    help: str


class Task(ABC):
    """Abstract Task class which handles the framework and writing to LaTeX files

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output"""

    def __init__(self):
        """Constructor setting the most important values to error strings"""
        self.cmd_info = None
        self.task_io = None

    @abstractmethod
    def init_argument_parser(self, parser) -> None:
        """Method for task specific argument initialization

        :param parser: the argparse parser"""

    @abstractmethod
    def parse(self, arg_input) -> None:
        """Parse function for arguments which are task specific

        :param arg_input: the result from argparser"""

    @abstractmethod
    def algorithm(self):
        """The algorithm for which this generator is generating exercises.
        Yield gives a tuple where the first is either a state of the program and
        the second is highlighting, which may be None
        or it may be an latex object which should be printed.

        :yield: intermediate steps of the algorithm"""

    @abstractmethod
    def generate_exercise(self) -> LatexObject:
        """Method to generate an exercise LaTeX file code

        :return: the ``LatexObject`` representing the exercise"""

    @abstractmethod
    def generate_solution(self) -> LatexObject:
        """Method to generate an solution LaTeX file code

        :return: the ``LatexObject`` representing the solution"""


__tasks_dict = {}
"""Dictionary for registrations of all tasks"""
__category_dict = {}
"""Dictionary containing the descriptions and cmds of all categories"""


def register_category(category: str, description: str, cmd_help: str):
    """
    Method to register a new category

    :param category: the cmd name for the category
    :param description: the cmd description for this category
    :param cmd_help: the cmd help text for this category
    """
    if category in __tasks_dict:
        raise ValueError(f"Tried to register {category}, but was already registered")
    __category_dict[category] = (description, cmd_help)
    __tasks_dict[category] = {}


def register_task(category: str, task: Task):
    """Method to register a task

    :param category: the cmd name of the category
    :param task: the cmd name of the task"""
    __tasks_dict[category][task.cmd_info.cmd] = task


def get_task_by_cmd(category: str, cmd: str) -> Task:
    """Method to look into the task registry

    :param category: the cmd name of the category
    :param cmd: the cmd name of the task
    :return: the task corresponding to this combination"""
    return __tasks_dict[category][cmd]


def get_category_info(category: str):
    """
    Method to get the cmd information for a category

    :param category: the cmd name for this category
    :return: a tuple containg first the description, then the help text of this category
    """
    return __category_dict[category]


def category_iterator():
    """The iterator for the categories

    :return: an iterator for the categories"""
    return iter(__tasks_dict)


def task_iterator(category: str):
    """Method to iterate over all tasks of one category

    :return: an iterator for all tasks fron this category"""
    return iter(__tasks_dict[category].values())


register_category(
    "misc",
    "Miscellaneous tasks",
    "Miscellaneous tasks that do not find any other category",
)
