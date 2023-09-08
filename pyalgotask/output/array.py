"""Outputs arrays with various special options"""
import dataclasses
import pylatex as latex
from pyalgotask.output import pylatex_classes as clatex

from pyalgotask.output.output_base import Output


@dataclasses.dataclass
class ArrayTaskInfo:
    """Dataclass to bundle task related data

    :ivar prefix: prefix of the task explanation
    :ivar task_array: the task_array of the task
    :ivar postfix: postfix of the task explanation"""

    prefix: str
    task_array: list
    postfix: str


@dataclasses.dataclass
class ArrayLatexOptions:
    """Dataclass to bundle latex related options

    :ivar phantom_length: the default phantom length for solution file
    :ivar preamble: preamble for the LaTeX file
    :ivar exercise_lengths_of_arrays: the length of the arrays as list
    :ivar exercise_left_labels: labels list for labels left of the array, if any, one per array
    :ivar exercise_top_labels: labels list list for labels above the array, if any.
            Label for every entry in array
    :ivar exercise_phantom_length: the default phantom length for the
                solution space in the exercise file"""

    phantom_length: int
    preamble: latex.base_classes.LatexObject
    exercise_lengths_of_arrays: int
    exercise_left_labels: list
    exercise_top_labels: list
    exercise_phantom_length: int


class ArrayOutput(Output):
    """Class to create LaTeX exercise and solution code for static array lengths

    :ivar task_info: information concerning the task description
    :ivar latex_option: various options regarding the latex output
    :ivar algorithm: the algorithm to generate the exercise for

    """

    def __init__(self, task_array, prefix, postfix, algorithm):
        """
        Constructor for arrays with fixed input

        :param task_array: the input array for the algorithm
        :param prefix: the prefix of the task explanation
        :param postfix: the postfix of the task explanation
        :param algorithm: the algorithm generator
        """
        self.task_info = ArrayTaskInfo(prefix, task_array, postfix)
        phantom_length = (
            2 if len(task_array) == 0 else max(len(str(x)) for x in task_array)
        )
        preamble = latex.Command("usetikzlibrary", "positioning")
        self.latex_options = ArrayLatexOptions(
            phantom_length,
            preamble,
            exercise_lengths_of_arrays=None,
            exercise_left_labels=None,
            exercise_top_labels=None,
            exercise_phantom_length=None,
        )
        self.algorithm = algorithm

    def init_argument_parser(self, parser) -> None:
        """No parsers needed herer."""

    def parse(self, args) -> None:
        """No parsers needed herer."""

    def init_exercise_output(
        self, *, lengths_of_arrays, phantom_length=2, left_labels=None, top_labels=None
    ):
        """
        Method to initialize data that is usually only known after parsing the input data.

        :param lengths_of_arrays: List of lengths of the arrays to use
        :param phantom_length: The length of the exercise solution space entries
        :param left_labels: A list of labels printed left of the arrays
        :param top_labels: A list of list of labels printed above each entry of the arrays
        """
        self.latex_options.exercise_lengths_of_arrays = lengths_of_arrays
        self.latex_options.exercise_left_labels = left_labels
        self.latex_options.exercise_top_labels = top_labels
        self.latex_options.exercise_phantom_length = phantom_length
        if (
            self.latex_options.phantom_length
            < self.latex_options.exercise_phantom_length
        ):
            self.latex_options.phantom_length = self.latex_options.exercise_phantom_length

    def get_exercise_preamble(self):
        return self.latex_options.preamble

    def get_solution_preamble(self):
        return self.latex_options.preamble

    def generate_exercise(self):
        """Generates a ``LatexObject`` consisting of the exercise without preamble"""
        container = clatex.EmptyContainer()

        self.generate_exercise_prefix(container)
        self.generate_exercise_space(container)

        return container

    def generate_solution(self):
        """Generates a ``LatexObject`` consisting of the solution without preamble"""
        container = clatex.EmptyContainer()

        self.generate_solution_prefix(container)
        self.generate_solution_space(container)

        return container

    def generate_exercise_prefix(self, container):
        """Fille an LaTeX Container with the task explanation

        :param container: The container that is filled"""
        container.append(latex.Command("noindent"))
        container.append(latex.NoEscape(self.task_info.prefix))
        container.append(clatex.Line(options="2ex"))

        tikz = self.create_tikz_array()
        self.task_array_to_tikz(tikz)

        container.append(latex.LargeText(tikz))
        container.append(clatex.Line(options="2ex"))

        container.append(latex.NoEscape(self.task_info.postfix))

        container.append(clatex.Line(options="4ex"))

    def generate_exercise_space(self, container):
        """Fille an LaTeX Container with the exercise solution space

        :param container: The container that is filled"""
        tikz = self.create_tikz_array()

        last_start_index = 0
        new_start_index = 0
        line_num = 0
        for array_length in self.latex_options.exercise_lengths_of_arrays:
            if new_start_index == 0:
                self.empty_tikz_array(tikz=tikz, length=array_length)
                if self.latex_options.exercise_left_labels:
                    self.tikz_array_left_label(
                        tikz,
                        new_start_index,
                        self.latex_options.exercise_left_labels[line_num],
                    )
                if self.latex_options.exercise_top_labels:
                    self.tikz_array_top_labels(
                        tikz,
                        new_start_index,
                        self.latex_options.exercise_top_labels[line_num],
                    )
                new_start_index += array_length
                line_num += 1
            else:
                first_options = (
                    "below=of n" + str(last_start_index)
                    if not self.latex_options.exercise_top_labels
                    else "below=4ex of n" + str(last_start_index)
                )
                self.empty_tikz_array(
                    tikz=tikz,
                    length=array_length,
                    tikz_start_index=new_start_index,
                    node_option_first=first_options,
                )
                if self.latex_options.exercise_left_labels:
                    self.tikz_array_left_label(
                        tikz,
                        new_start_index,
                        self.latex_options.exercise_left_labels[line_num],
                    )
                if self.latex_options.exercise_top_labels:
                    self.tikz_array_top_labels(
                        tikz,
                        new_start_index,
                        self.latex_options.exercise_top_labels[line_num],
                    )
                last_start_index = new_start_index
                new_start_index += array_length
                line_num += 1

        container.append(tikz)

    def generate_solution_prefix(self, container):
        """Fille an LaTeX Container with the solution explanation

        :param container: The container that is filled"""

    def generate_solution_space(self, container):
        """Fille an LaTeX Container with the actual solution

        :param container: The container that is filled"""
        last_start_index = 0
        new_start_index = 0
        line_num = 0

        tikz = self.create_tikz_array()
        self.task_array_to_tikz(tikz=tikz)

        new_start_index += len(self.task_info.task_array)

        for array, highlights in self.algorithm():
            self.filled_tikz_array(
                tikz=tikz,
                array=array,
                tikz_start_index=new_start_index,
                highlights=highlights,
                node_option_first="below=of n" + str(last_start_index),
            )

            if self.latex_options.exercise_left_labels:
                self.tikz_array_left_label(
                    tikz,
                    new_start_index,
                    label=self.latex_options.exercise_left_labels[line_num],
                )
            if self.latex_options.exercise_top_labels:
                self.tikz_array_top_labels(
                    tikz,
                    new_start_index,
                    labels=self.latex_options.exercise_top_labels[line_num],
                )
            last_start_index = new_start_index
            new_start_index += max(len(array), 1)
            line_num += 1

        container.append(tikz)

    def task_array_to_tikz(
        self, tikz, *, new_start_index=0, highlights=None, node_options_first=""
    ):
        """
        Fills the tikz environment ``tikz`` with ``self.task_array`` using the given parameters.

        :param tikz: the tikz environment to fill
        :param new_start_index: the first index the array should start with
        :param highlights: the array where each entry signifies the node should be highlighted
        :param node_options_first: Special additional options for the first node
        """

        self.filled_tikz_array(
            tikz=tikz,
            array=self.task_info.task_array,
            tikz_start_index=new_start_index,
            highlights=highlights,
            node_option_first=node_options_first,
        )
        return tikz

    def create_tikz_array(self):
        """
        Creates a tikz array environment, i.e. an tikz environment with fitting style options.

        :return: tikz environment with array styles
        """
        options = latex.NoEscape(
            (
                "node/.style={rectangle,draw=black,thick,inner sep=5pt}, "
                "highlight/.style={fill=gray!30}, node distance=0.25 and 0"
            )
        )
        return latex.TikZ(options=options)

    def zero_length_tikz_array(self, tikz, *, tikz_start_index=0, first_options=""):
        """
        Fills the tikz environment with an array of length zero

        :param tikz: the tikz environment to fill
        :param tikz_start_index: the index where the first node should start
        :param first_options: special options for the first node
        """
        tikz.append(
            latex.TikZNode(
                handle="n" + str(tikz_start_index),
                options=first_options,
                text=clatex.StringEmptyContainer(
                    clatex.PhantomLength(self.latex_options.phantom_length)
                ),
            )
        )

    def empty_tikz_array(
        self, tikz, length, *, node_option="", tikz_start_index=0, node_option_first=""
    ):
        """
        Fills the tikz environment with an empty array of given length

        :param tikz: the tikz environment to fill
        :param length: the length of the array
        :param node_option: style options for the node
        :param tikz_start_index: the start index for the first node
        :param node_option_first: special style options for the first node
        """

        first_options = filter(None, ["node", node_option, node_option_first])

        if length < 1:
            self.zero_length_tikz_array(
                tikz, tikz_start_index=tikz_start_index, first_options=first_options
            )

        tikz.append(
            latex.TikZNode(
                handle="n" + str(tikz_start_index),
                options=first_options,
                text=clatex.StringEmptyContainer(
                    clatex.PhantomLength(self.latex_options.phantom_length)
                ),
            )
        )

        for i in range(1, length):
            options = filter(
                None,
                ["node", "right=of n" + str(tikz_start_index + i - 1), node_option],
            )

            tikz.append(
                latex.TikZNode(
                    handle="n" + str(tikz_start_index + i),
                    options=options,
                    text=clatex.StringEmptyContainer(
                        clatex.PhantomLength(self.latex_options.phantom_length)
                    ),
                )
            )

    def filled_tikz_array(
        self,
        tikz,
        array,
        *,
        highlights=None,
        node_option="",
        highlight_option="highlight",
        tikz_start_index=0,
        node_option_first="",
    ):
        """
        Fills the tikz environment with an given array

        :param tikz: the tikz environment to fill
        :param array: the array to fill the tikz environment
        :param highlights: a list where each entry signifies whether highlights should be used
        :param node_option: style options for the node
        :param highlight_option: which style options should be used for highlights
        :param tikz_start_index: the start index for the first node
        :param node_option_first: special style options for the first node
        """

        first_options = filter(
            None,
            [
                "node",
                node_option,
                node_option_first,
                highlight_option if highlights and highlights[0] else "",
            ],
        )

        if len(array) < 1:
            self.zero_length_tikz_array(
                tikz, tikz_start_index=tikz_start_index, first_options=first_options
            )
            return

        max_str_length = max(len(str(i)) for i in array)

        diff = max_str_length - len(str(array[0]))

        container = clatex.StringEmptyContainer()
        container.append(clatex.VPhantomLength())
        container.append(clatex.PhantomLength(diff))
        container.append(latex.NoEscape(str(array[0])))

        tikz.append(
            latex.TikZNode(
                handle="n" + str(tikz_start_index),
                options=first_options,
                text=container,
            )
        )

        for i in range(1, len(array)):
            diff = max_str_length - len(str(array[i]))
            options = filter(
                None,
                [
                    "node",
                    "right=of n" + str(tikz_start_index + i - 1),
                    node_option,
                    highlight_option if highlights and highlights[i] else "",
                ],
            )

            container = clatex.StringEmptyContainer()
            container.append(clatex.VPhantomLength())
            container.append(clatex.PhantomLength(diff))
            container.append(latex.NoEscape(str(array[i])))

            tikz.append(
                latex.TikZNode(
                    handle="n" + str(tikz_start_index + i),
                    options=options,
                    text=container,
                )
            )

    def tikz_array_left_label(self, tikz, start_index, label):
        """
        Creates labels left of the array with start_index

        :param tikz: the tikz environment
        :param start_index: the start_index of the array where the label should be created for
        :param label: the label
        """
        tikz.append(
            latex.TikZNode(
                handle="left_label" + str(start_index),
                options="left=of n" + str(start_index),
                text=label,
            )
        )

    def tikz_array_top_labels(self, tikz, start_index, labels):
        """
        Creates labels over the array with start_index

        :param tikz: the tikz environment
        :param start_index: the start_index of the array where the labels should be created for
        :param labels: the labels
        """
        i = start_index
        for label in labels:
            tikz.append(
                latex.TikZNode(
                    handle="top_label" + str(i),
                    options="above=of n" + str(i),
                    text=label,
                )
            )
            i += 1


class AlgorithmArrayOutput(ArrayOutput):
    """Class to create LaTeX exercise and solution code for algorithm generated arrays

    :ivar prefix: the prefix text for the exercise (i.e. before the input array)
    :ivar task_array: the input for the algorithm
    :ivar phantom_length: the default phantom length for solution file
    :ivar postfix: the postfix text for the exercise (i.e. after the input array)
    :ivar algorithm: the algorithm to generate the exercise for
    :ivar preamble: preamble for the LaTeX file
    :ivar exercise_left_labels: labels list for labels left of the array, if any, one per array
    :ivar exercise_top_labels: labels list list for labels above the array, if any.
            Label for every entry in array
    :ivar exercise_phantom_length: the default phantom length for the
                solution space in the exercise file
    """

    def __init__(self, task_array, prefix, postfix, algorithm):
        """
        Constructor for arrays with fixed input

        :param task_array: the input array for the algorithm
        :param prefix: the prefix of the task explanation
        :param postfix: the postfix of the task explanation
        :param algorithm: the algorithm generator
        """
        super().__init__(task_array, prefix, postfix, algorithm)
        self.exercise_num_of_additional_arrays = 0

    init_exercise_output = None
    """Please use init_exercise_algorithm_output!"""

    def init_exercise_algorithm_output(self, *, num_of_additional_arrays=0):
        """
        Method to initialize data that is usually only known after parsing the input data.

        :param num_of_additional_arrays: List of lengths of the arrays to use
        """
        self.exercise_num_of_additional_arrays = num_of_additional_arrays

    def generate_exercise_space(self, container):
        """Fille an LaTeX Container with the exercise solution space.
        Lengths are determined by the algorithm.

        :param container: The container that is filled"""
        tikz = self.create_tikz_array()

        output = list(self.algorithm())
        if len(output) == 0:
            return

        max_array_length = max(len(array) for (array, _) in output)

        last_start_index = 0
        new_start_index = 0
        for array, _ in output:
            array_length = max(len(array), 1)
            if new_start_index == 0:
                self.empty_tikz_array(tikz=tikz, length=array_length)
                new_start_index += array_length
            else:
                self.empty_tikz_array(
                    tikz=tikz,
                    length=array_length,
                    tikz_start_index=new_start_index,
                    node_option_first="below=of n" + str(last_start_index),
                )
                last_start_index = new_start_index
                new_start_index += array_length

        for _ in range(self.exercise_num_of_additional_arrays):
            self.empty_tikz_array(
                tikz=tikz,
                length=max_array_length,
                tikz_start_index=new_start_index,
                node_option_first="below=of n" + str(last_start_index),
            )
            last_start_index = new_start_index
            new_start_index += max_array_length

        container.append(tikz)


class OperationsArrayOutput(ArrayOutput):
    """Class to generate LaTeX code when using operations on an array and static array length

    :ivar prefix: the prefix text for the exercise (i.e. before the input array)
    :ivar task_array: the input for the algorithm
    :ivar phantom_length: the default phantom length for solution file
    :ivar postfix: the postfix text for the exercise (i.e. after the input array)
    :ivar algorithm: the algorithm to generate the exercise for
    :ivar preamble: preamble for the LaTeX file
    :ivar exercise_lengths_of_arrays: the length of the arrays as list
    :ivar exercise_left_labels: labels list for labels left of the array, if any, one per array
    :ivar exercise_top_labels: labels list list for labels above the array, if any.
            Label for every entry in array
    :ivar exercise_phantom_length: the default phantom length for the
                solution space in the exercise file
    """

    def __init__(self, operations, prefix, postfix, algorithm):
        """
        Constructor for arrays over operations with fixed input

        :param operations: the input operations for the algorithm
        :param prefix: the prefix of the task explanation
        :param postfix: the postfix of the task explanation
        :param algorithm: the algorithm generator
        """
        super().__init__([], prefix, postfix, algorithm)
        self.operations = operations
        self.phantom_length = max(len(str(x.value)) for x in self.operations)

    def generate_exercise_prefix(self, container):
        """Fille an LaTeX Container with the task explanation over lists of operations

        :param container: The container that is filled"""
        container.append(latex.Command("noindent"))
        container.append(latex.NoEscape(self.task_info.prefix))

        latex_list = latex.Enumerate()

        for operation in self.operations:
            latex_list.add_item(latex.NoEscape(str(operation)))

        container.append(latex_list)

        container.append(latex.NoEscape(self.task_info.postfix))

        container.append(clatex.Line(options="4ex"))

    def generate_solution_space(self, container):
        """Fille an LaTeX Container with the actual solution.
        It does not repeat the task_array here.

        :param container: The container that is filled"""
        last_start_index = 0
        new_start_index = 0
        line_num = 0

        tikz = self.create_tikz_array()

        for array, highlights in self.algorithm():
            node_option_first = (
                "" if new_start_index == 0 else "below=of n" + str(last_start_index)
            )
            self.filled_tikz_array(
                tikz=tikz,
                array=array,
                tikz_start_index=new_start_index,
                highlights=highlights,
                node_option_first=node_option_first,
            )
            if self.latex_options.exercise_left_labels:
                self.tikz_array_left_label(
                    tikz,
                    new_start_index,
                    self.latex_options.exercise_left_labels[line_num],
                )
            if self.latex_options.exercise_top_labels:
                self.tikz_array_top_labels(
                    tikz,
                    new_start_index,
                    self.latex_options.exercise_top_labels[line_num],
                )
            last_start_index = new_start_index
            new_start_index += max(len(array), 1)
            line_num += 1

        container.append(tikz)
