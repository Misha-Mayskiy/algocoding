import math


class NoArgsError(Exception):
    pass


class TupleFormatError(Exception):
    pass


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def people(*args):
    if not args:
        raise NoArgsError("Arguments are not passed")

    result = []
    for item in args:
        if not isinstance(item, tuple) or len(item) != 2 or not isinstance(item[0], str) or not isinstance(item[1],
                                                                                                           int):
            raise TupleFormatError("Invalid tuple format")

        text, number = item

        if number == 0:
            raise ZeroDivisionError("You can't divide by zero")

        if len(text) % number == 0 and is_prime(number) and text.islower():
            result.append(text)

    return result
