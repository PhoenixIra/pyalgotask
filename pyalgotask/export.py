"""Module to export pylatex classes into a file, compile it and view it in the internal viewer"""
import logging
import webbrowser

import pylatex as latex

_logger = logging.getLogger(__name__)


class Exporter:
    """Class for exporting pylatex classes to exercise and solution files

    :ivar exercise_tex_file: The file location of the exercise tex file
    :ivar solution_tex_file: The file location of the solution tex file
    :ivar pdf: Whether a pdf should be generated
    :ivar view: Whether an pdf should be generated and viewed afterwards
    """

    def __init__(self):
        """Initializes every member variable with None and False respectively"""
        self.exercise_tex_file = None
        self.solution_tex_file = None
        self.pdf = False
        self.view = False

    def init_parser(self, parser):
        """
        Initialized the arguments for file locations of exercise and solution and compile options.

        :param parser: The argparse parser for command-line argument parsing
        """
        parser.add_argument(
            "-e",
            "--exercise",
            type=str,
            dest="exercise_tex",
            default="exercise",
            help="The file where the exercise description will be saved to without file extension.",
        )
        parser.add_argument(
            "-s",
            "--solution",
            type=str,
            dest="solution_tex",
            default="solution",
            help="The file where the solution description will be saved to without file extension.",
        )
        parser.add_argument(
            "--pdf",
            action="store_true",
            dest="pdf",
            help="If set, a pdf will be generated.",
        )
        parser.add_argument(
            "--view",
            action="store_true",
            dest="view",
            help="If set, a pdf will be generated and viewed afterwards.",
        )

    def parse(self, input_arguments):
        """
        Function to parse input data from argparse

        :param input_arguments: The input handing from the argparse parser to further parse
        """
        self.exercise_tex_file = input_arguments.exercise_tex
        self.solution_tex_file = input_arguments.solution_tex
        self.pdf = input_arguments.pdf
        self.view = input_arguments.view
        logging.debug(
            "Parsed pathes to export to: %s %s",
            self.exercise_tex_file,
            self.solution_tex_file,
        )
        if not self.exercise_tex_file and not self.solution_tex_file:
            _logger.error("No output specified! Did you forget to specify -e or -s?")

    def write_exercise(self, task) -> str:
        """
        Method to write the generated exercise LaTeX file code

        :param task: The task for which to create the exercise file

        :return: A string consisting of the LaTeX code for the task
        """
        if self.exercise_tex_file:
            doc = latex.Document()
            doc.preamble.append(task.task_io.output.get_exercise_preamble())
            doc.append(task.task_io.output.generate_exercise())
            if not self.pdf and not self.view:
                doc.generate_tex(self.exercise_tex_file)
            else:
                doc.generate_pdf(self.exercise_tex_file)
            if self.view:
                webbrowser.open_new(self.exercise_tex_file + ".pdf")

    def write_solution(self, task) -> str:
        """
        Method to write the generated solution LaTeX file code

        :param task: the task for which to create the exercise file

        :return: A string consisting of the LaTeX code for the task
        """
        if self.solution_tex_file:
            doc = latex.Document()
            doc.preamble.append(task.task_io.output.get_solution_preamble())
            doc.append(task.task_io.output.generate_solution())
            if not self.pdf and not self.view:
                doc.generate_tex(self.solution_tex_file)
            else:
                doc.generate_pdf(self.solution_tex_file)
            if self.view:
                webbrowser.open_new(self.solution_tex_file + ".pdf")
