"""Various classes extending the capabilities of pylatex."""
from pylatex.base_classes import Container, CommandBase
from pylatex import TikZNode, Command


class EmptyContainer(Container):
    """An empty container for capsulating functionalities"""

    def dumps(self):
        """dumps its content without any surrounding"""
        return self.dumps_content()


class Line(CommandBase):
    """A linebreak using doubleslash instead of \\newline"""

    def __init__(self, arguments=None, options=None, *, extra_arguments=None):
        """
        Sete the ``_latex_name`` correctly and calls the super constructor

        :param arguments: The main arguments of the command.
        :param options: Options of the command. These are placed in front of the arguments.
        :param extra_arguments:  Extra arguments for the command. When these are supplied the
            options will be placed before them instead of before the normal
            arguments. This allows for a way of having one or more arguments
            before the options.
        """
        super().__init__(
            arguments=arguments, options=options, extra_arguments=extra_arguments
        )
        self._latex_name = "\\"


class EmptyLine(CommandBase):
    """An empty line with an space followed by double slash"""

    def __init__(self, arguments=None, options=None, *, extra_arguments=None):
        """
        Sete the ``_latex_name`` correctly and calls the super constructor

        :param arguments: The main arguments of the command.
        :param options: Options of the command. These are placed in front of the arguments.
        :param extra_arguments:  Extra arguments for the command. When these are supplied the
            options will be placed before them instead of before the normal
            arguments. This allows for a way of having one or more arguments
            before the options.
        """
        super().__init__(
            arguments=arguments, options=options, extra_arguments=extra_arguments
        )
        self._latex_name = " \\\\"


class PhantomLength(CommandBase):
    """Phantom with predfined input in various length"""

    def __init__(self, length=2):
        """
        Sete the ``_latex_name`` correctly and calls the super constructor

        :param length: number of A for the phantom
        """
        super().__init__(arguments="A" * length)
        self._latex_name = "phantom"


class VPhantomLength(CommandBase):
    """VPhantom with predfined input in various length"""

    def __init__(self, length=1):
        """
        Sete the ``_latex_name`` correctly and calls the super constructor

        :param length: number of A for the vphantom
        """
        super().__init__(arguments="A" * length)
        self._latex_name = "vphantom"


class StringEmptyContainer(EmptyContainer):
    """LaTeX Container with string content"""

    def __init__(self, *args, **kwargs):
        """
        Sete the ``_latex_name`` correctly and calls the super constructor

        :param args: The string inside the container
        :param kwargs: Extra arguments for the command. When these are supplied the
            options will be placed before them instead of before the normal
            arguments. This allows for a way of having one or more arguments
            before the options.
        """
        super().__init__(**kwargs)
        for arg in args:
            self.append(arg)
        self.content_separator = " "

    def dumps(self):
        """dumps its content without any surrounding"""
        return self.dumps_content()

    def __repr__(self):  ##pylint: disable=invalid-repr-returned
        """returns dumps()"""
        return self.dumps()


class SlashlessCommand(Command):
    """
    Command without slash in the front
    """

    def dumps(self):
        """Represent the command as a string in LaTeX syntax.

        :return: The LaTeX formatted command
        """

        options = self.options.dumps()  # pylint: disable=no-member
        arguments = self.arguments.dumps()  # pylint: disable=no-member

        if self.extra_arguments is None:
            return f"{self.latex_name}{options}{arguments}"

        extra_arguments = self.extra_arguments.dumps()

        return f"{self.latex_name}{arguments}{options}{extra_arguments}"


class TikZBinaryTreeNode(TikZNode):
    """A class that represents a TiKZ node with tree children."""

    tab_number = 1

    def __init__(
        self, handle=None, options=None, at=None, text=None, left=None, right=None
    ):  # pylint: disable=too-many-arguments
        """

        :param handle: Node identifier
        :param options: List of options
        :param at: Coordinate where node is placed
        :param text: Body text of the node
        :param children: list of children TikZTreeNodes
        """
        super().__init__(handle, options, at, text)
        self.left = left
        self.right = right

    def dumps(self):
        """Return string representation of the node."""

        ret_str = []
        if TikZBinaryTreeNode.tab_number == 1:
            ret_str.append(Command("node", options=self.options).dumps())
        else:
            ret_str.append(SlashlessCommand("node", options=self.options).dumps())

        if self.handle is not None:
            ret_str.append(f"({self.handle})")

        if self._node_position is not None:
            ret_str.append(f"at {str(self._position)}")

        if self._node_text is not None:
            ret_str.append(f"{{{self._node_text}}}")
        else:
            ret_str.append("{}")

        nodes = []
        nodes.append(" ".join(ret_str))

        TikZBinaryTreeNode.tab_number += 1

        if self.left is not None:
            nodes.append(
                "    " * TikZBinaryTreeNode.tab_number
                + f"child [left=23] {{{self.left.dumps()}}}"
            )
        if self.right is not None:
            nodes.append(
                "    " * TikZBinaryTreeNode.tab_number
                + f"child [right=23] {{{self.right.dumps()}}}"
            )

        TikZBinaryTreeNode.tab_number -= 1

        if TikZBinaryTreeNode.tab_number == 1:
            return "%\n".join(nodes) + ";"
        return "%\n".join(nodes)
