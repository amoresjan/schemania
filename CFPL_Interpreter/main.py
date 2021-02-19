from tokenizer import tokenizer
from parse_tokens import *
from var_table import ValuesTable

while True:
    lines = input(">> ")

    tokens = tokenizer(lines)
    # print(tokens)

    output = Parser(tokens)

    if (tokens[0])[0] == "VAR":
        print(output.parse_declaration())
        print(ValuesTable.val)

    if (tokens[0])[1] == "identifier":
        output.parse_assign()
        print(ValuesTable.val)

    if (tokens[0])[1] == "INPUT":
        print(tokens)
        assign_token = []
        assign_value = []

        input_lines = input(">> Enter Values: ")  # 3,4
        input_tokens = tokenizer(input_lines)

        for token in input_tokens:
            if not token[1] == "comma":
                assign_value.append(token)

        i = 0
        for token in tokens:
            if token[1] == "identifier":
                assign_token.append(token)
                assign_token.append(("=", "assignment"))
                try:
                    assign_token.append(assign_value[i])
                except:
                    raise Exception("Input Wrong")
                i += 1

        if len(assign_value) != i:
            raise Exception("Input Wrong")

        for i in range(0, len(assign_token), 3):
            input_assign = Parser(assign_token[i:i+3])
            input_assign.parse_assign()

        print(ValuesTable.val)

        # for i in range(len(assign_token)):

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
