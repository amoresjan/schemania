from var_table import ValuesTable


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def keep(self, token_type):
        if self.current_token[1] == token_type:
            self.advance()
        else:
            raise Exception("Invalid Syntax")

    def parse_declaration(self):
        var_tokens = []

        if self.current_token[1] == 'VAR':
            self.advance()

            # var_tokens.append(self.current_token[0])
            value = ('null', "un-identified")
            identifier = self.current_token
            var_tokens.append((identifier, value))
            self.keep("identifier")

            while self.current_token[1] == 'comma' or self.current_token[1] == 'assignment':

                if self.current_token[1] == 'assignment':
                    self.keep("assignment")

                    value = self.current_token
                    var_tokens[len(var_tokens)-1] = (identifier, value)
                    self.advance()

                else:
                    self.keep("comma")

                    identifier = self.current_token
                    var_tokens.append((identifier, value))
                    self.keep("identifier")

            self.keep("AS")

            dataType = self.current_token[0]
            for i, var in enumerate(var_tokens):
                iden = var[0]
                val = var[1]

                if val[1] == "un-identified":

                    if dataType == "INT":
                        val = ('0', "integer")
                    elif dataType == "FLOAT":
                        val = ('0.0', "float")
                    elif dataType == "CHAR":
                        val = (val[0], "char")
                    elif dataType == "BOOL":
                        val = (val[0], "bool")
                    var_tokens[i] = (iden, val)

                flag = False
                if (dataType == "INT" and val[1] == "integer") or (dataType == "FLOAT" and val[1] == "float") or (dataType == "CHAR" and val[1] == "char") or (dataType == "BOOL" and val[1] == "bool"):
                    flag = True

                if flag:
                    ValuesTable.add_var(iden[0][0], val)
                else:
                    self.keep("error")  # temporary error handler

            self.keep("data_types")

        return var_tokens

    def parse_assign(self):   # assigns a value to a variable
        var_identifiers = []

        value_index = max(index for index, item in enumerate(
            self.tokens) if item == ("=", "assignment")) + 1

        tempValueholder = self.tokens[value_index:]
        self.tokens = self.tokens[:value_index]

        if self.current_token[1] == "identifier" and ValuesTable.check_var(self.current_token[0]):
            var_identifiers.append(self.current_token)
            self.advance()

            self.keep("assignment")

            if self.pos != len(self.tokens):
                while self.current_token[1] == "identifier":
                    if not ValuesTable.check_var(self.current_token[0]):
                        # temporary error handler
                        self.keep("error identifier not initialize")

                    var_identifiers.append(self.current_token)
                    self.keep("identifier")
                    self.keep("assignment")

                    if self.pos == len(self.tokens):
                        break
        else:
            self.keep("error identifier not initialize")

        token_value = []

        for token in tempValueholder:
            if token[1] == "identifier" and ValuesTable.check_var(token[0]):
                token_value.append(ValuesTable.get_var(token[0]))
            else:
                token_value.append(token)

        if (token_value[0])[1] == "bool" or (token_value[0])[1] == "char":
            charORbool = "bool" if (token_value[0])[1] == "bool" else "char"

            if charORbool == "bool":
                if (token_value[0])[0] != "TRUE" or (token_value[0])[0] != "FALSE":
                    raise Exception("Bool value is not TRUE or FALSE")

            for identifier in var_identifiers:
                if (ValuesTable.get_var(identifier[0]))[1] == charORbool:
                    ValuesTable.add_var(identifier[0], token_value)
                else:
                    if charORbool == "bool":
                        # temporary error handler
                        self.keep("error identifier is a char")
                    else:
                        # temporary error handler
                        self.keep("error identifier is a bool")

        else:
            value, token = parse_exp(token_value)

            for identifier in var_identifiers:
                if (ValuesTable.get_var(identifier[0]))[1] == "integer":
                    val = (int(value), "integer")
                else:
                    val = (value, "float")
                ValuesTable.add_var(identifier[0], val)


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


def parse_exp(tokens: list):    # computes arithmetic expressions with precedence rules
    operator_stack = []
    expression_stack = []

    tokens.append((')', "parenthesis"))

    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token[0] == "(":
            value, tokens = parse_exp(tokens[i + 1:])
            i = -1

            expression_stack.append(value)

        elif token[1] == "integer" or token[1] == "float":
            expression_stack.append(float(token[0]))

        elif token[1] == "identifier":
            value = ValuesTable.get_var(token[0])
            expression_stack.append(float(value))

        elif token[1] == "operators":
            while len(operator_stack) and precedence[token[0]] <= precedence[operator_stack[-1]]:
                operator = operator_stack.pop()
                operand_2 = expression_stack.pop()
                operand_1 = expression_stack.pop()

                value = operator_mapping[operator](operand_1, operand_2)
                expression_stack.append(value)

            operator_stack.append(token[0])

        elif token[0] == ")":
            while len(operator_stack):
                operator = operator_stack.pop()
                operand_2 = expression_stack.pop()
                operand_1 = expression_stack.pop()

                value = operator_mapping[operator](operand_1, operand_2)
                expression_stack.append(value)

            return expression_stack[-1], tokens[i + 1:-1]

        i += 1

# from var_table import *
# from validate import Validate
#


#
#
# def parse_declaration(tokens: list):  # only checks a single line for validity
#     valid = Validate()
#     keys = []
#     values = [0, "TYPE"]
#     if valid.is_valid_syntax(tokens):
#         i = 0
#         for token in tokens:
#             if token[1] == "identifier":
#                 ValuesTable.add_var(token[0], values)
#                 keys.append(token[0])
#
#             if token[1] == "data_types":
#                 for name in keys:
#                     ValuesTable.val.get(name)[1] = token[0]
#                 keys.clear()
#
#         return print(ValuesTable.val)
#
#     else:
#         raise Exception("Invalid Syntax")
#
#
# def parse_tokens(tokens: list):
#     # if tokens[1][0] == "=":
#     #     parse_ass(tokens)
#     # else:
#     #     return parse_exp(tokens)[0]
#     return parse_declaration(tokens)
