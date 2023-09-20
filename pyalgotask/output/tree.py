"""Outputs arrays with various special options"""
import dataclasses
import pylatex as latex
from pylatex.base_classes import LatexObject

from pyalgotask.output import pylatex_classes as clatex
from pyalgotask.output.output_base import Output


@dataclasses.dataclass
class TreeTaskInfo:
    """Dataclass to bundle task related data

    :ivar prefix: prefix of the task explanation
    :ivar operation: the operations of the task
    :ivar postfix: postfix of the task explanation"""

    prefix: str
    operations: list
    postfix: str


@dataclasses.dataclass
class TreeLatexOptions:
    """Dataclass to bundle latex related options

    :ivar one_column: whether the trees should be in one column (instead of two)
    :ivar exercise_preamble: preamble for the exercise LaTeX file
    :ivar solution_preamble: preamble for the solution LaTeX file"""

    exercise_preamble: latex.base_classes.LatexObject
    solution_preamble: latex.base_classes.LatexObject
    one_column: bool


class TreeOutput(Output):
    """Outputs tasks with tree structures.

    :ivar task_info: information concerning the task description
    :ivar latex_option: various options regarding the latex output
    :ivar algorithm: the algorithm to generate the exercise for
    :ivar _indent_depth: helper variable to keep track of the indentation depth
    """

    def __init__(
        self, operations, exercise_prefix, exercise_postfix, algorithm
    ) -> None:
        super().__init__()
        self.one_column = False
        self.task_info = TreeTaskInfo(exercise_prefix, operations, exercise_postfix)
        exercise_preamble = clatex.EmptyContainer()
        solution_preamble = latex.Command("usetikzlibrary", "positioning")
        self.latex_options = TreeLatexOptions(
            exercise_preamble=exercise_preamble,
            solution_preamble=solution_preamble,
            one_column=False,
        )
        self.algorithm = algorithm
        self._indent_depth = 0

    def init_argument_parser(self, parser) -> None:
        """
        Method for input specific argument initialization

        :param parser: The argparser subparser to init arguments to
        """
        parser.add_argument(
            "--one-column",
            dest="one_column",
            action="store_true",
            help="Generates the solution in one column instead of two.",
        )

    def parse(self, args) -> None:
        """
        Method for parsing the input

        :param args: The output of the argparser parser
        """
        self.one_column = args.one_column

    def get_exercise_preamble(self):
        return self.latex_options.exercise_preamble

    def get_solution_preamble(self):
        return self.latex_options.solution_preamble

    def generate_exercise(self) -> LatexObject:
        """Fills an LaTeX Container with the task explanation over lists of operations

        :param container: The container that is filled"""
        container = clatex.EmptyContainer()
        container.append(latex.Command("noindent"))
        container.append(latex.NoEscape(self.task_info.prefix))

        latex_list = latex.Enumerate()

        for operation in self.task_info.operations:
            latex_list.add_item(latex.NoEscape(str(operation)))

        container.append(latex_list)

        container.append(latex.NoEscape(self.task_info.postfix))

        container.append(clatex.Line(options="4ex"))
        return container

    def generate_solution(self) -> LatexObject:
        """
        Method for generating the LaTeX source code for the solution sheet.

        :return: A base LaTeX object from pylatex containg the solution sheet.
        """
        container = clatex.EmptyContainer()

        if self.latex_options.one_column:
            for tree, label in self.algorithm():
                container.append(latex.NoEscape(label))
                container.append(clatex.Line(options="2ex"))
                tikz = self.create_tikz_tree()
                self.draw_tree_with_label(tikz, tree)
                center = latex.Center()
                center.append(tikz)
                container.append(center)
                container.append(clatex.Line(options="2ex"))
        else:
            left = True
            for tree, label in self.algorithm():
                minipage = latex.MiniPage(width=r"0.45\textwidth")
                minipage.append(latex.NoEscape(label))
                minipage.append(clatex.Line(options="2ex"))
                tikz = self.create_tikz_tree()
                self.draw_tree_with_label(tikz, tree)
                center = latex.Center()
                center.append(tikz)
                minipage.append(center)
                container.append(minipage)
                if left:
                    left = False
                else:
                    container.append(clatex.Line(options="2ex"))
                    left = True

        return container

    def create_tikz_tree(self):
        """Creates a tikz environment for the tree"""
        return latex.TikZ(
            options=latex.NoEscape("every node/.append style={circle, draw, sibling angle=25}")
        )

    def create_visitor_for_node(self):
        """Method to generate a visitor that generates nodes for each tree node.
        Can be overwritten to make special trees layouts

        :return: a visitor for the tree class"""

        self._indent_depth = 0

        def visitor_node_create(node):
            self._indent_depth += 1
            return clatex.TikZBinaryTreeNode(
                handle=str(self._indent_depth), text=str(node.value)
            )

        return visitor_node_create

    def draw_tree_with_label(self, tikz, tree):
        """Method to iterate through the tree in order to generate a tree representation in LaTeX

        :param tikz: an tikz environment
        :param tree: the tree class"""

        nodes = tree.visitor(self.create_visitor_for_node())

        def tuple_to_node(tree_in_tuple_form):
            if tree_in_tuple_form is None:
                return None
            (root, left, right) = tree_in_tuple_form

            left_tree = tuple_to_node(left)
            if left_tree is not None:
                root.left = left_tree

            right_tree = tuple_to_node(right)
            if right_tree is not None:
                root.right = right_tree

            return root

        tree = tuple_to_node(nodes)

        tikz.append(tree)
