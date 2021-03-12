precedence = {
    "-": 1,
    "+": 1,
    "*": 2,
    "/": 2,
    "%": 2,
}


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def modulo(a, b):
    return a % b


operator_mapping = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "%": modulo,
}


def greater_than(a, b):
    return a > b


def lesser_than(a, b):
    return a < b


def greater_equal(a, b):
    return a >= b


def lesser_equal(a, b):
    return a <= b


def equal(a, b):
    return a == b


def not_equal(a, b):
    return a != b


comparison_mapping = {
    ">": greater_than,
    "<": lesser_than,
    ">=": greater_equal,
    "<=": lesser_equal,
    "==": equal,
    "<>": not_equal,
}

logic_precedence = {
    "NOT": 3,
    "AND": 2,
    "OR": 1,
}


def and_logic(a, b):
    return a and b


def or_logic(a, b):
    return a or b


def not_logic(a):
    return not a


logical_mapping = {
    "AND": and_logic,
    "OR": or_logic,
    "NOT": not_logic
}
