"""Reads an operation sequence for use in datastructures"""
import pathlib
import logging

from pyalgotask.structures.operation import Operation, OperationType

from pyalgotask.input.input_base import Input

_logger = logging.getLogger(__name__)


def str_to_in_del_int(arg: str) -> tuple[Operation, int]:
    """
    Casting method from string to delete and insert operations.

    :param arg: a string to convert into a delete or an insert operation
    :return: A delete or an insert operation object corresponding to x."""
    val = int(arg[1:])

    result = None
    if arg[0] == "+":
        result = Operation(OperationType.INSERT, val)
    elif arg[0] == "-":
        result = Operation(OperationType.DELETE, val)
    else:
        raise ValueError(f"Not a valid operator: {arg[0]}")

    return result


class InDelOperators(Input):
    """
    Class for parsing insert and delete operations for use in datastructure tasks.

    :ivar cast_function: internal cast function for the array entries
    :ivar data: the parsed operations for other classes to access
    """

    def __init__(self, cast_function=str_to_in_del_int):
        """Calls the super class, sets the cast function (default str_to_del_in) and
        sets the operations list to None"""
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
                "The file with the input operations. The file should only have "
                "one line consisting of a comma separated list of elements either with "
                "a + (insert) or a minus (delete)."
            ),
        )
        group.add_argument(
            "-i",
            "--input",
            type=str,
            dest="input",
            help=(
                "The input operations consisting of of a comma separated "
                "list of elements either with a + (insert) or a minus (delete)."
            ),
        )

    def parse(self, args) -> None:
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
