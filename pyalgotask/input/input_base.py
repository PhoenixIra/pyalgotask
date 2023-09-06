"""Base Modul for input classes. This defines a rough base structure to rely on."""
from abc import ABC, abstractmethod


class Input(ABC):
    """
    Abstract base input class guarateeing methods to initialize a parser and
    to parse the output of argparse
    """

    def __init__(self):
        """
        Initialized the data field to None
        """
        self.data = None

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
