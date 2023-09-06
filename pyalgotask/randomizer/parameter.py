"""Module for a random integer parameter"""
from random import Random
from . import randomizer_base


class IntParameterRandomizer(randomizer_base.Randomizer):
    """Randomizer to generate a random integer parameter

    :ivar min_value: the minimal value to sample from
    :ivar max_value: the maximal value to sample from
    :ivar operations_length: the number of operations that should be sampled
    :ivar deletion_probability: the probability a delete happens, given that this is even possible
    :ivar last_result: to regain the values last sampled
    :ivar random: the random number generator"""

    def __init__(
        self,
        min_value=0,
        max_value=99,
        seed: int = None,
        *,
        random_generator: Random = None,
        parameter_name: str,
    ):
        """Constructor to set default values and the PRNG

        :param min_value: the minimal value as integer to sample from
        :param max_value: the maximal value as integer to sample from
        :param seed: the seed of the PRNG
        :param random_generator: a custom RNG
        :param parameter_name: the name of the parameter for the parser"""
        super().__init__(seed=seed, random_generator=random_generator)
        self.name = parameter_name
        self.min_value = min_value
        self.max_value = max_value

    def init_argument_parser(self, parser):
        """Method to initialise the argparser and set new arguments.

        :param parser: the argparser to set arguments for"""
        parser.add_argument(
            f"--min-{self.name}",
            dest=f"random_min_{self.name}",
            type=int,
            help=f"Minimal bound for paramter {self.name}",
            default=self.min_value,
        )
        parser.add_argument(
            f"--max-{self.name}",
            dest=f"random_max_{self.name}",
            type=int,
            help=f"Maximal bound for paramter {self.name}",
            default=self.max_value,
        )

    def parse(self, arg_input):
        """Method to parse the arguments after argparse parsed them

        :param arg_input: the result of argparse"""
        self.min_value = getattr(arg_input, f"random_min_{self.name}")
        self.max_value = getattr(arg_input, f"random_max_{self.name}")

    def get_random_input(self):
        """Method to generate a random input

        :return: a sample from the input"""
        self.last_result = self.random.randrange(self.min_value, self.max_value)
        return self.last_result


class FloatParameterRandomizer(randomizer_base.Randomizer):
    """Randomizer to generate a random float parameter

    :ivar min_value: the minimal value to sample from
    :ivar max_value: the maximal value to sample from
    :ivar operations_length: the number of operations that should be sampled
    :ivar deletion_probability: the probability a delete happens, given that this is even possible
    :ivar last_result: to regain the values last sampled
    :ivar random: the random number generator"""

    def __init__(
        self,
        min_value=0,
        max_value=1,
        seed: int = None,
        *,
        random_generator: Random = None,
        parameter_name: str,
    ):
        """Constructor to set default values and the PRNG

        :param min_value: the minimal value as integer to sample from
        :param max_value: the maximal value as integer to sample from
        :param seed: the seed of the PRNG
        :param random_generator: a custom RNG
        :param parameter_name: the name of the parameter for the parser"""
        super().__init__(seed=seed, random_generator=random_generator)
        self.name = parameter_name
        self.min_value = min_value
        self.max_value = max_value

    def init_argument_parser(self, parser):
        """Method to initialise the argparser and set new arguments.

        :param parser: the argparser to set arguments for"""
        parser.add_argument(
            f"--min-{self.name}",
            dest=f"random_min_{self.name}",
            type=float,
            help=f"Minimal bound for paramter {self.name}",
            default=self.min_value,
        )
        parser.add_argument(
            f"--max-{self.name}",
            dest=f"random_max_{self.name}",
            type=float,
            help=f"Maximal bound for paramter {self.name}",
            default=self.max_value,
        )

    def parse(self, arg_input):
        """Method to parse the arguments after argparse parsed them

        :param arg_input: the result of argparse"""
        self.min_value = getattr(arg_input, f"random_min_{self.name}")
        self.max_value = getattr(arg_input, f"random_max_{self.name}")

    def get_random_input(self):
        """Method to generate a random input

        :return: a sample from the input"""
        self.last_result = self.random.uniform(self.min_value, self.max_value)
        return self.last_result
