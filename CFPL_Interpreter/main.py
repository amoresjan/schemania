from tokenizer import tokenizer
from parse_tokens import parse_tokens
from validate import Validate
from var_table import *

while True:
    lines = input(">> ")

    tokens = tokenizer(lines)
    # print(tokens)

    # v = Validate()
    # print("Valid : ", v.is_valid_syntax(tokens))

    for token in tokens:
        if token[1] == "identifier":
            print("Variable = ", token[0])

    # output = parse_tokens(tokens)
    #
    # if output is not None:
    #     print(output)

# values = [0]
# ValuesTable.add_var("x", values)
# values.append("INT")
# #
# print(ValuesTable.val)

# TypeTable.add_var("x", "INT")
# TypeTable.add_var("y", "INT")
#
# print(TypeTable.type)
