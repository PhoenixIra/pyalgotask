"""Various classes extending the capabilities of pylatex."""
from pylatex.base_classes import Container, CommandBase


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
