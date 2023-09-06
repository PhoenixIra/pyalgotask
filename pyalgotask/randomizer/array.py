"""Randomizer for arrays with various input types"""
from random import Random
from ..randomizer import randomizer_base


class RandomIntArray(randomizer_base.Randomizer):
    """Randomizer to generate integer arrays

    :ivar min_value: the minimal value to sample from
    :ivar max_value: the maximal value to sample from
    :ivar array_length: the length of the array to generate
    :ivar last_result: to regain the values last sampled
    :ivar random: the random number generator"""

    def __init__(
        self,
        min_value=0,
        max_value=99,
        seed: int = None,
        *,
        random_generator: Random = None,
    ):
        """Constructor allowing to set the min and max values to sample from and
        a custom seed or RNG

        :param seed: a custom seed for the PRNG
        :param random_generator: a custom RNG
        :param min_value: the minimal value to sample from
        :param max_value: the maximal value to sample from"""
        super().__init__(seed=seed, random_generator=random_generator)
        self.min_value = min_value
        self.max_value = max_value
        self.array_length = 6

    def init_argument_parser(self, parser):
        """Method to initialise the argparser and set new arguments.

        :param parser: the argparser to set arguments for"""
        parser.add_argument(
            "--random_int_range",
            dest="random_int_range",
            help=(
                "The minimal and maximal integer a "
                "randomized array should have values from"
            ),
            type=int,
            nargs=2,
            default=[self.min_value, self.max_value],
        )
        parser.add_argument(
            "--random_array_length",
            dest="random_array_length",
            help="The length of the randomized array",
            type=int,
            default=self.array_length,
        )

    def parse(self, arg_input):
        """Method to parse the min value, max value and array length
          after argparse parsed them

        :param arg_input: the result of argparse"""
        if arg_input.random_int_range[0] > arg_input.random_int_range[1]:
            raise ValueError(
                (
                    "minimal int is not less than or equal to maximal int: "
                    f"min {arg_input.random_int_range[0]} vs "
                    f"max {arg_input.random_int_range[1]}"
                )
            )
        self.min_value = arg_input.random_int_range[0]
        self.max_value = arg_input.random_int_range[1]
        self.array_length = arg_input.random_array_length

    def get_random_input(self):
        """Method to generate a random input

        :return: a sample from the input"""
        result = self.random.choices(
            population=range(self.min_value, self.max_value), k=self.array_length
        )
        self.last_result = result
        return result


class RandomFloatArray(randomizer_base.Randomizer):
    """Randomizer to generate float arrays

    :ivar min_value: the minimal value to sample from
    :ivar max_value: the maximal value to sample from
    :ivar array_length: the length of the array to generate
    :ivar precision: the precision of the floats as sampled
    :ivar last_result: to regain the values last sampled
    :ivar random: the random number generator"""

    def __init__(
        self,
        min_value=0,
        max_value=0.99,
        seed: int = None,
        *,
        random_generator: Random = None,
    ):
        """Constructor allowing to set the min and max values to sample from and
        a custom seed or RNG

        :param seed: a custom seed for the PRNG
        :param random_generator: a custom RNG
        :param min_value: the minimal value to sample from
        :param max_value: the maximal value to sample from"""
        super().__init__(seed=seed, random_generator=random_generator)
        self.min_value = min_value
        self.max_value = max_value
        self.array_length = 6
        self.precision = 2

    def init_argument_parser(self, parser):
        parser.add_argument(
            "--random_int_range",
            dest="random_float_range",
            help=(
                "The minimal and maximal float "
                "a randomized array should have values from"
            ),
            type=float,
            nargs=2,
            default=[self.min_value, self.max_value],
        )
        parser.add_argument(
            "--random_array_length",
            dest="random_array_length",
            help="The length of the randomized array",
            type=int,
            default=self.array_length,
        )
        parser.add_argument(
            "--precision",
            dest="random_precision",
            help="Precision of the floating numbers in number of decimal points",
            type=int,
            default=self.precision,
        )

    def parse(self, arg_input):
        """Method to parse the arguments after argparse parsed them

        :param arg_input: the result of argparse"""
        if arg_input.random_float_range[0] > arg_input.random_float_range[1]:
            raise ValueError(
                (
                    "minimal float is not less than or equal to maximal float: "
                    f"min {arg_input.random_float_range[0]} vs "
                    f"max {arg_input.random_float_range[1]}"
                )
            )
        self.min_value = arg_input.random_float_range[0]
        self.max_value = arg_input.random_float_range[1]
        self.array_length = arg_input.random_array_length
        self.precision = arg_input.random_precision

    def get_random_input(self):
        """Method to generate a random input

        :return: a sample from the input"""
        result = []
        for _ in range(0, self.array_length):
            result.append(
                round(
                    self.random.uniform(self.min_value, self.max_value), self.precision
                )
            )
        self.last_result = result
        return result
