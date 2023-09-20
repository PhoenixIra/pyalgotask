"""Base class for Output classes offering methods to use the argument parser and
to generate exercise and solution source code."""
from abc import ABC, abstractmethod
from pylatex.base_classes import LatexObject


class Output(ABC):
    "Base class for Output classes."

    @abstractmethod
    def init_argument_parser(self, parser) -> None:
        """
        Method for input specific argument initialization

        :param parser: The argparser subparser to init arguments to
        """

    @abstractmethod
    def parse(self, args) -> None:
        """
        Method for parsing the input

        :param args: The output of the argparser parser
        """

    def get_exercise_preamble(self) -> LatexObject:
        """
        Getter for the preamble designated for the exercise sheet.
        
        :return: A base LaTeX object from pylatex containing the preamble for the exercise sheet"""

    def get_solution_preamble(self) -> LatexObject:
        """
        Getter for the preamble designated for the solution sheet.
        
        :return: A base LaTeX object from pylatex containing the preamble for the solution sheet"""

    @abstractmethod
    def generate_exercise(self) -> LatexObject:
        """
        Method for generating the LaTeX source code for the exercise sheet.

        :return: A base LaTeX object from pylatex containing the exercise sheet.
        """

    @abstractmethod
    def generate_solution(self) -> LatexObject:
        """
        Method for generating the LaTeX source code for the solution sheet.

        :return: A base LaTeX object from pylatex containing the solution sheet.
        """
