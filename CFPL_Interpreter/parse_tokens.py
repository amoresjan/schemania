from var_table import ValuesTable
from operations import *
from tokenizer import tokenizer


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

    def parse_program(self):
        self.parse_declarations_block()
        self.parse_code_block()

    def parse_declarations_block(self):
        while self.current_token[1] == 'VAR':
            self.parse_declaration()

    def parse_declaration(self):
        var_tokens = []

        if self.current_token[1] == 'VAR':
            self.advance()

            value = ('null', "un-identified")
            identifier = self.current_token
            var_tokens.append((identifier, value))
            self.keep("identifier")

            while self.current_token[1] == 'comma' or self.current_token[1] == 'assignment':
                if self.current_token[1] == 'assignment':
                    self.keep("assignment")
                    value = self.current_token
                    var_tokens[len(var_tokens) - 1] = (identifier, value)
                    self.advance()

                else:
                    self.keep("comma")
                    identifier = self.current_token
                    var_tokens.append((identifier, value))
                    self.keep("identifier")

            self.keep("AS")
            self.type_assign(var_tokens)
            self.keep("data_types")

    def type_assign(self, var_tokens):
        data_type = self.current_token[0]

        for i, var in enumerate(var_tokens):
            iden = var[0]
            val = var[1]

            if val[1] == "un-identified":
                if data_type == "INT":
                    val = ('0', "integer")
                elif data_type == "FLOAT":
                    val = ('0.0', "float")
                elif data_type == "CHAR":
                    val = ('', "char")
                elif data_type == "BOOL":
                    val = ('"FALSE"', "bool")
                var_tokens[i] = (iden, val)

            flag = False
            if (data_type == "INT" and val[1] == "integer") or (data_type == "FLOAT" and val[1] == "float") or (
                    data_type == "CHAR" and val[1] == "char") or (data_type == "BOOL" and val[1] == "bool"):
                flag = True

            if flag:
                ValuesTable.add_var(iden[0], val)
            else:
                self.keep("error")  # temporary error handler

    def parse_code_block(self):
        self.keep("START")
        self.parse_statements_block()
        self.keep("STOP")

    def parse_statements_block(self):
        while self.current_token[1] != 'STOP':
            if self.current_token[1] == 'EOF':
                raise Exception("No STOP keyword")
            self.parse_code_statements()

    def parse_code_statements(self):
        if self.current_token[0] == '*' and (
                self.tokens[self.pos + 1][1] != 'float' or self.tokens[self.pos + 1][1] != 'float'):
            pass  # comment statements

        elif self.current_token[1] == 'INPUT':
            self.advance()
            self.parse_input()

        elif self.current_token[1] == 'OUTPUT':
            pass  # output statements

        elif self.current_token[1] == 'identifier':
            self.parse_assign()

    def parse_input(self):
        assign_token = []
        assign_value = []

        input_lines = input(">> Enter Values: ")  # 3,4
        input_tokens = tokenizer(input_lines)

        for token in input_tokens:
            if not token[1] == "comma":
                assign_value.append(token)

        i = 0
        assign_token.append(self.current_token)
        assign_token.append(("=", "assignment"))
        assign_token.append(assign_value[i])
        self.keep("identifier")
        i += 1
        while self.current_token[1] == 'comma':
            self.keep("comma")
            assign_token.append(self.current_token)
            assign_token.append(("=", "assignment"))
            self.keep("identifier")
            if assign_value[i][1] != 'EOF':
                assign_token.append(assign_value[i])
            else:
                raise Exception("Expected more inputs")
            i += 1

        if (len(assign_value)-1) != i:
            raise Exception("Expected less inputs")  # input values is greater than identifiers

        for i in range(0, len(assign_token), 3):
            input_assign = Parser(assign_token[i:i + 3])
            input_assign.parse_assign()

    def parse_assign(self):  # assigns a value to a variable
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
                if (token_value[0])[0] not in ['"TRUE"', '"FALSE"']:
                    raise Exception("Bool value is not TRUE or FALSE")

            for identifier in var_identifiers:
                if (ValuesTable.get_var(identifier[0]))[1] == charORbool:
                    ValuesTable.add_var(identifier[0], token_value[0])
                else:
                    if charORbool == "bool":
                        # temporary error handler
                        self.keep("error identifier is a char")
                    else:
                        # temporary error handler
                        self.keep("error identifier is a bool")

        else:
            value, token = self.parse_exp(token_value)

            for identifier in var_identifiers:
                if (ValuesTable.get_var(identifier[0]))[1] == "integer":
                    val = (int(value), "integer")
                else:
                    val = (value, "float")
                ValuesTable.add_var(identifier[0], val)

    def parse_exp(self, tokens):  # computes arithmetic expressions with precedence rules
        operator_stack = []
        expression_stack = []

        tokens.append((')', "parenthesis"))

        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token[0] == "(":
                value, tokens = self.parse_exp(tokens[i + 1:])
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
