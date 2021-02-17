
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

            var_tokens.append(self.current_token[0])
            self.keep("identifier")

            while self.current_token[1] == 'comma':
                self.keep("comma")
                var_tokens.append(self.current_token[0])
                self.keep("identifier")

            self.keep("AS")

            self.keep("data_types")

        return var_tokens


# from var_table import *
# from validate import Validate
#
# precedence = {
#     "-": 1,
#     "+": 1,
#     "*": 2,
#     "/": 2,
#     "%": 2,
# }
#
#
# def add(a, b):
#     return a + b
#
#
# def subtract(a, b):
#     return a - b
#
#
# def multiply(a, b):
#     return a * b
#
#
# def divide(a, b):
#     return a / b
#
#
# def modulo(a, b):
#     return a % b
#
#
# operator_mapping = {
#     "+": add,
#     "-": subtract,
#     "*": multiply,
#     "/": divide,
#     "%": modulo,
# }
#
#
# def parse_exp(tokens: list):    # computes arithmetic expressions with precedence rules
#     operator_stack = []
#     expression_stack = []
#
#     tokens.append((')', "parenthesis"))
#
#     i = 0
#
#     while i < len(tokens):
#         token = tokens[i]
#
#         if token[0] == "(":
#             value, tokens = parse_exp(tokens[i + 1:])
#             i = -1
#
#             expression_stack.append(value)
#
#         elif token[1] == "numbers":
#             expression_stack.append(float(token[0]))
#
#         elif token[1] == "identifier":
#             value = ValuesTable.find_var(token[0])
#             expression_stack.append(float(value))
#
#         elif token[1] == "operators":
#             while len(operator_stack) and precedence[token[0]] <= precedence[operator_stack[-1]]:
#                 operator = operator_stack.pop()
#                 operand_2 = expression_stack.pop()
#                 operand_1 = expression_stack.pop()
#
#                 value = operator_mapping[operator](operand_1, operand_2)
#                 expression_stack.append(value)
#
#             operator_stack.append(token[0])
#
#         elif token[0] == ")":
#             while len(operator_stack):
#                 operator = operator_stack.pop()
#                 operand_2 = expression_stack.pop()
#                 operand_1 = expression_stack.pop()
#
#                 value = operator_mapping[operator](operand_1, operand_2)
#                 expression_stack.append(value)
#
#             return expression_stack[-1], tokens[i + 1:-1]
#
#         i += 1
#
#
# def parse_ass(tokens: list):    # assigns a value to a variable
#     name = tokens[0][0]
#     value = tokens[2:]
#     value, tokens = parse_exp(value)
#
#     ValuesTable.add_var(name, value)
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
