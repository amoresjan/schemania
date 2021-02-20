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
