"""Main module for pyAlgoTask handling calling other classes and the general work flow."""
import argparse
import sys
import logging

import pyalgotask.__meta as meta
import pyalgotask.__settings as settings
import pyalgotask.tasks.task_base as task_base

from pyalgotask.export import Exporter

# let every task register itself
import pyalgotask.tasks  # pylint: disable=unused-import


logging.basicConfig(level=settings.LOGGING_LEVEL)

logger = logging.getLogger(__name__)


def main():
    """Main method of the algorithm and is called when executing the program on the folder."""

    # create argument parser
    logger.debug("Creating argument parser.")
    parser = argparse.ArgumentParser(
        prog="pyAlgoEx",
        description="Generates exercises for your typical algorithms course.",
        epilog=(
            "Choose an algorithm for which an exercise is generated.\n"
            "If you choose no input method, a random input will be generated.\n"
            "If you choose no output file path, the generated files will not be written anywhere."
        ),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {meta.__version__}",
    )

    exporter = Exporter()
    subparser = parser.add_subparsers(title="Task categories", dest="cat")
    subparser.metavar = ""
    cat_parsers = {}

    for cat in task_base.category_iterator():
        (help_string, description) = task_base.get_category_info(cat)
        cat_parser = subparser.add_parser(
            cat, help=help_string, description=description
        )
        cat_parsers[cat] = cat_parser
        cat_subparser = cat_parser.add_subparsers(dest="cmd")
        for this_task in task_base.task_iterator(cat):
            task_parser = cat_subparser.add_parser(
                this_task.cmd_info.cmd,
                help=this_task.cmd_info.help,
                description=this_task.cmd_info.description,
            )
            exporter.init_parser(task_parser)
            this_task.init_argument_parser(task_parser)

    # parse arguments
    logger.debug("Argument parser working.")
    try:
        args = parser.parse_args()
    except ValueError as exception:
        parser.error(exception)

    # send help if no arguments present
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    if not args.cat:
        parser.error("No category given!")

    if not args.cmd:
        cat_parsers[args.cat].print_help()
        sys.exit()

    # get requested task
    this_task = task_base.get_task_by_cmd(args.cat, args.cmd)
    logger.debug("Selected task: %s %s", args.cat, args.cmd)

    # parse arguments for task
    try:
        exporter.parse(args)
        this_task.parse(args)
    except ValueError as exception:
        parser.error(str(exception))
    logger.debug("Arguments parsed by task %s.", this_task.cmd_info.cmd)

    # write exercise to file
    logger.debug("Writing exercise.")
    try:
        exporter.write_exercise(this_task)
    except ValueError as exception:
        parser.error(str(exception))

    # write solution to file
    logger.debug("Writing solution.")
    try:
        exporter.write_solution(this_task)
    except ValueError as exception:
        parser.error(str(exception))


if __name__ == "__main__":
    main()
