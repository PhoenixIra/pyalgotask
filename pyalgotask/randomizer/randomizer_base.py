"""Base class for randomizers to guarantee uniformity"""
from abc import ABC, abstractmethod
from random import Random


class Randomizer(ABC):
    """A randomizer needs access to the parser and offers a method to generate
    a sample from the input.

    :ivar random: the random number generator
    :ivar last_result: the last result which was sampled
    :ivar max_value: the maximal value to sample
    :ivar min_value: the minimal value to sample"""

    def __init__(self, seed: int = None, *, random_generator: Random = None):
        """Constructor allowing to set a custom seed or RNG

        :param seed: a custom seed for the PRNG
        :param random_generator: a custom RNG"""
        if random_generator:
            self.random = random_generator
        else:
            self.random = Random(seed)
        self.last_result = None
        self.min_value = None
        self.max_value = None

    @abstractmethod
    def init_argument_parser(self, parser):
        """Method to initialise the argparser and set new arguments.

        :param parser: the argparser to set arguments for"""

    @abstractmethod
    def parse(self, arg_input):
        """Method to parse the arguments after argparse parsed them

        :param arg_input: the result of argparse"""

    @abstractmethod
    def get_random_input(self):
        """Method to generate a random input

        :return: a sample from the input"""
