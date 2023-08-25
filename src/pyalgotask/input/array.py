"""Reads array inputs for algorithms such as sorting algorithms"""
import pathlib
import logging

from .input_base import Input

_logger = logging.getLogger(__name__)


class ArrayInput(Input):
    """Class to handle arrays as input, as well as their input syntax.

    :ivar cast_function: internal cast function for the array entries
    :ivar data: internal array for other methods to access"""

    def __init__(self, cast_function=int):
        """Calls the super class, sets the cast function (default int()) and
        sets the internal array to None"""
        super().__init__()
        self.cast_function = cast_function

    def init_argument_parser(self, parser) -> None:
        """
        Method for input specific argument initialization

        :param parser: The argparser subparser to init arguments to
        """
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-f",
            "--file",
            type=pathlib.Path,
            dest="file",
            help=(
                "The file with input array. The file should only have one line "
                "consisting of a comma separated list of input elements that python "
                "will always interpret as strings."
            ),
        )
        group.add_argument(
            "-i",
            "--input",
            type=str,
            dest="input",
            help=(
                "The input array consisting of a comma separated list of "
                "input elements that python will always interpret as strings."
            ),
        )

    def parse(self, args):
        """
        Method for parsing the input

        :param args: The output of the argparser parser
        """
        if args.file is not None:
            with open(args.file, "r", encoding="UTF-8") as file:
                line = file.readline()
            self.data = list(map(self.cast_function, line.split(",")))
        elif args.input is not None:
            self.data = list(map(self.cast_function, args.input.split(",")))
        else:
            self.data = None
        _logger.debug("Parsed input: %s", self.data)
