from tokenizer import tokenizer
from parse_tokens import *
from validate import Validate
from var_table import *

while True:
    lines = input(">> ")

    tokens = tokenizer(lines)
    # print(tokens)

    output = Parser(tokens)
    print(output.parse_declaration())



    # v = Validate()
    # print("Valid : ", v.is_valid_syntax(tokens))

    # for token in tokens:
    #     if token[1] == "identifier":
    #         print("Variable = ", token[0])

    # output = parse_tokens(tokens)
    #
    # if output is not None:
    #     print(output)

# values = [0]
# ValuesTable.add_var("x", values)
# values.append("INT")
# #
# print(ValuesTable.val)
