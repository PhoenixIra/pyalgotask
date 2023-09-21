"""Modul to randomize insert and delete operations"""
from pyalgotask.randomizer import randomizer_base
from pyalgotask.structures.operation import Operation, OperationType


class RandomInDelOperations(randomizer_base.Randomizer):
    """Randomizer to generate integer insert and delete operations

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
        operations_length=6,
        seed=None,
        *,
        random_generator=None,
        deletion_probability=0.1,
    ):
        """Constructor to set default values and the PRNG

        :param min_value: the minimal value as integer to sample from
        :param max_value: the maximal value as integer to sample from
        :param operations_length: the number of operations that should be sampled
        :param seed: the seed of the PRNG
        :param random_generator: a custom RNG
        :param deletion_probability: the default probability that a delete will ocure next,
            given that something can be deleted"""
        super().__init__(seed=seed, random_generator=random_generator)
        self.min_value = min_value
        self.max_value = max_value
        self.operations_length = operations_length
        self.deletion_probability = deletion_probability

    def init_argument_parser(self, parser):
        """Method to initialise the argparser and set new arguments.

        :param parser: the argparser to set arguments for"""
        parser.add_argument(
            "--random_int_range",
            dest="random_int_range",
            help=(
                "The minimal and maximal integer a randomized array "
                "should have values from"
            ),
            type=int,
            nargs=2,
            default=[self.min_value, self.max_value],
        )
        parser.add_argument(
            "--random_number_of_operations",
            dest="random_operations_length",
            help="The number of the randomly choosen operations",
            type=int,
            default=self.operations_length,
        )
        parser.add_argument(
            "--del-prob",
            dest="random_del_prob",
            help="Sets the probability of an operation beeing deletions",
            type=float,
            default=self.deletion_probability,
        )

    def parse(self, arg_input):
        """Method to parse min value, max value, operations length
         and deletion probability after argparse parsed them

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
        self.operations_length = arg_input.random_operations_length
        self.deletion_probability = arg_input.random_del_prob

    def get_random_input(self) -> tuple[Operation, int]:
        """Method to generate a random input

        :return: a sample from the input"""
        op_nums = [-1]
        while min(op_nums) < 0:
            random_operations = self.random.choices(
                population=[0, 1],
                weights=[self.deletion_probability, 1 - self.deletion_probability],
                k=self.operations_length,
            )
            op_nums, op_num = [], 0
            for is_insert in random_operations:
                op_num += 2 * is_insert - 1
                op_nums.append(op_num)

        not_insert_values = set(range(self.min_value, self.max_value))
        insert_values = set()
        result = []
        for is_insert in random_operations:
            if is_insert:
                operation = Operation(
                    OperationType.INSERT, self.random.choice(list(not_insert_values))
                )
                insert_values.add(operation[1])
                not_insert_values.remove(operation[1])
            else:
                operation = Operation(
                    OperationType.DELETE, self.random.choice(list(insert_values))
                )
                insert_values.remove(operation.value)
                not_insert_values.add(operation.value)
            result.append(operation)
        self.last_result = result
        return result
