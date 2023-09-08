"""Module for tasks with open hashing"""
from pyalgotask import language as lang

from pyalgotask.tasks import task_base
from pyalgotask.structures import OperationType
from pyalgotask.tasks.hashing import hashing_base


class ChainingHashing(hashing_base.Hashing):
    """Open Hashing as in Cormen, Leiserson, Rivest, Stein.
    Introduction to Algorithms 4ed. 2022. MIT Press, page 278

    :ivar cmd_info: a bundle of cmd information
    :ivar task_io: an TaskIO object containing a parser, randomizer and output
    :ivar hashtable_size: the size of the hash table to use
    :ivar hash_function: the (first) hash function to use
    :ivar exercise_texts: prefix and postfix of the task description
    :ivar operations: the operation to apply to the hash table
    """

    def __init__(self):
        """Initialized cmd and exercise text information"""
        super().__init__()
        self.cmd_info = task_base.TaskCmd(
            cmd="chaining",
            description=(
                "Exercise to apply open hashing (i.e. chaining) "
                "on insert and delete operations into hashtables."
            ),
            help="Open hashing (i.e. chaining) for operations on integers.",
        )
        self.exercise_texts[0] = lang.get_text("hashing", "chaining-prefix")
        self.exercise_texts[1] = lang.get_text("hashing", "chaining-postfix")

    def init_hashing_argument_parser(self, parser):
        """No additinal arguments required

        :param parser: argparser parser object"""

    def parse_hashing(self, arg_input):
        """Checks how many places the lists should have

        :param arg_input: result of the argparser
        """
        max_op_num = 0
        op_num = 0
        for operation in self.operations:
            if operation.is_operation_type(OperationType.INSERT):
                op_num += 1
            if operation.is_operation_type(OperationType.DELETE):
                op_num -= 1
            if op_num < 0:
                raise ValueError(
                    f"More delete operations before insertion operations found at {operation}"
                )
            max_op_num = max(max_op_num, op_num)

        lengths = [max_op_num for i in range(0, self.hashtable_size)]

        labels = [str(i) + ":" for i in range(0, self.hashtable_size)]

        self.task_io.output.init_exercise_output(
            lengths_of_arrays=lengths, left_labels=labels
        )

    def algorithm(self):
        """
        The hashing algorithm using chaining

        :yield: the hash table after all operations
        """
        hashtable = [[] for _ in range(self.hashtable_size)]

        for operation in self.operations:
            if operation.is_operation_type(OperationType.INSERT):
                if not self.insert(hashtable, operation.value):
                    raise AssertionError(
                        "Insert into hashtable failed! This should not have happend!"
                    )
            elif operation.is_operation_type(OperationType.DELETE):
                if not self.delete(hashtable, operation.value):
                    raise ValueError(
                        f"Operation {operation.type} not succesfull, "
                        "as it deletes something not existent."
                    )
            else:
                raise NotImplementedError(
                    f"Operator {operation.type} not supported by task {self.__class__.__name__}"
                )

        for hashentries in hashtable:
            yield ((hashentries, None))

    def insert(self, hashtable, value):
        """
        Inserting into a hashtable using chaining

        :param hashtable: the hashtable to insert intro
        :param value: the value to insert
        """
        hash_value = self.hash_function(value)
        if value not in hashtable[hash_value]:
            hashtable[hash_value].insert(0, value)
        return True

    def delete(self, hashtable, value):
        """
        Deleting from a hashtable using chaining

        :param hashtable: the hashtable to delete from
        :param value: the value to delete
        """
        hash_value = self.hash_function(value)
        if value in hashtable[hash_value]:
            hashtable[hash_value].remove(value)
            return True
        return False


task_base.register_task("hashing", ChainingHashing())
