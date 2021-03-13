from var_table import ValuesTable
from operations import *
from tokenizer import tokenizer
from constants import *


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

    def retreat(self):
        self.pos -= 1
        if self.pos > -1:
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def keep(self, token_type):
        if self.current_token[1] == token_type:
            self.advance()
        else:
            self.error("Invalid Syntax")

    def error(self, message):
        raise Exception(message)

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
            if self.current_token[1] in RESERVED_KEYWORDS:
                self.error("Variable %s invalid" % str(self.current_token[1]))
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
                    if self.current_token[1] in RESERVED_KEYWORDS:
                        self.error("Variable %s invalid" % str(self.current_token[1]))
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
                    val = ('FALSE', "bool")
                # var_tokens[i] = (iden, val)

            flag = False
            if (data_type == "INT" and val[1] == "integer") or \
                    (data_type == "FLOAT" and (val[1] == "float" or val[1] == "integer")) or \
                    (data_type == "CHAR" and val[1] == "char") or (data_type == "BOOL" and val[1] == "bool"):

                flag = True

                if val[1] == "bool":
                    val = (val[0].replace("\"", ""), "bool")

                # if token type of value assigned is an integer but datatype is float (e.g. x = 5 AS FLOAT)
                if data_type == "FLOAT":
                    val = (float(val[0]), "float")

                # to remove + (unary symbol) since its unnecessary
                if data_type == "INT":
                    val = (int(val[0]), "integer")

            if flag:
                ValuesTable.add_var(iden[0], val)
            else:
                self.error("error")  # temporary error handler

    def parse_code_block(self):
        self.keep("START")
        self.parse_statements_block()
        self.keep("STOP")

    def parse_statements_block(self):
        while self.current_token[1] != 'STOP':
            if self.current_token[1] == 'EOF':
                self.error("No STOP keyword")
            self.parse_code_statements()

    def parse_code_statements(self):
        if self.current_token[0] == '*' and (
                self.tokens[self.pos + 1][1] != 'float' or self.tokens[self.pos + 1][1] != 'float'):
            pass  # comment statements

        elif self.current_token[1] == 'INPUT':
            self.advance()
            self.parse_input()

        elif self.current_token[1] == 'OUTPUT':
            self.advance()
            self.parse_output()

        elif self.current_token[1] == 'IF':
            self.keep("IF")
            self.parse_if()

        elif self.current_token[1] == 'WHILE':
            self.keep('WHILE')
            self.parse_while()

        elif self.current_token[1] == 'identifier':
            self.parse_assign()

    def parse_input(self):
        assign_token = []
        assign_value = []

        input_lines = input(">>: ")  # 3,4
        input_tokens = tokenizer(input_lines)

        for token in input_tokens:
            if not token[1] == "comma":
                if token[1] == 'bool':
                    val = (token[0].replace("\"", ""), token[1])
                    token = val
                assign_value.append(token)

        i = 0
        assign_token.append(self.current_token)
        assign_token.append(("=", "assignment"))
        assign_token.append(assign_value[i])
        assign_token.append(("INPUT", "INPUT"))
        self.keep("identifier")
        i += 1
        while self.current_token[1] == 'comma':
            self.keep("comma")
            assign_token.append(self.current_token)
            assign_token.append(("=", "assignment"))
            self.keep("identifier")
            if assign_value[i][1] != 'EOF':
                assign_token.append(assign_value[i])
                assign_token.append(("INPUT", "INPUT"))
            else:
                self.error("Expected more inputs")
            i += 1

        if (len(assign_value) - 1) != i:
            # input values is greater than identifiers
            self.error("Expected less inputs")

        for i in range(0, len(assign_token), 4):
            input_assign = Parser(assign_token[i:i + 4])
            input_assign.parse_assign()

    def parse_output(self):
        output = ''

        while self.current_token[1] != 'STOP':
            token = self.current_token

            if token[1] == "ampersand":
                self.keep('ampersand')
                continue
            elif token[1] == "bool":
                output = output + str(token[0].replace("\"", ""))
                self.keep('bool')
            elif token[1] == "string":
                output = output + str(token[0].replace("\"", ""))
                self.keep('string')
            elif token[1] == "identifier":
                output = output + str(ValuesTable.get_var(token[0])[0])
                self.keep('identifier')
            elif token[1] == "integer" or token[1] == "float":
                output = output + str(token[0])
                self.advance()
            else:
                break

        print(output)

    def parse_if(self):
        bool_exp_length = self.assign_limit()
        bool_exp = self.tokens[self.pos + 1: bool_exp_length - 1]

        if len(bool_exp) == 0:
            bool_exp = self.tokens[self.pos + 1: bool_exp_length]

        self.keep('lparen')
        token_values = self.get_values(bool_exp)
        flag, token = self.parse_logical_exp(token_values)
        self.keep('rparen')

        if flag:
            self.parse_code_block()

            # if current token is ELSE, find end of code block
            if self.current_token[1] == 'ELSE':
                self.keep('ELSE')
                self.keep('START')
                while self.current_token[1] != 'STOP':
                    self.advance()
                self.keep('STOP')
        else:
            while self.current_token[1] != 'STOP':
                self.advance()
            self.keep('STOP')
            if self.current_token[1] == 'ELSE':
                self.keep('ELSE')
                self.parse_code_block()

            if self.current_token[1] == 'ELSE':
                self.error("ELSE statement should follow the IF statement")

    def parse_while(self):
        bool_exp_length = self.assign_limit()
        bool_exp = self.tokens[self.pos + 1: bool_exp_length - 1]
        while_index = self.pos - 1

        if len(bool_exp) == 0:
            bool_exp = self.tokens[self.pos + 1: bool_exp_length]

        self.keep('lparen')
        token_values = self.get_values(bool_exp)
        flag, token = self.parse_logical_exp(token_values)
        self.keep('rparen')

        stop_index = self.get_stop_index()

        while flag:
            self.parse_code_block()
            while self.pos != while_index:
                self.retreat()
            self.keep('WHILE')

            self.keep('lparen')
            token_values = self.get_values(bool_exp)
            flag, token = self.parse_logical_exp(token_values)
            self.keep('rparen')

        while self.pos != stop_index:
            self.advance()
        self.keep('STOP')

    def parse_assign(self):  # assigns a value to a variable
        var_identifiers = []
        value_index = self.assignment_index()
        max_limit = self.assign_limit()
        tempValueholder = self.tokens[value_index: max_limit]
        tokens = self.tokens[:value_index]

        # get identifiers which will receive the value
        if self.current_token[1] == "identifier" and ValuesTable.check_var(self.current_token[0]):
            var_identifiers.append(self.current_token)
            self.advance()

            self.keep("assignment")

            if self.pos != len(tokens):
                while self.current_token[1] == "identifier":
                    if not ValuesTable.check_var(self.current_token[0]):
                        # temporary error handler
                        self.error("error identifier not initialize")

                    var_identifiers.append(self.current_token)
                    self.keep("identifier")
                    self.keep("assignment")

                    if self.pos == len(tokens):
                        break

        else:
            self.error("error identifier not initialize")

        # assign the value to the receiving identifiers
        token_value = self.get_values(tempValueholder)

        if (ValuesTable.get_var((var_identifiers[0])[0]))[1] == "bool":
            value, token = self.parse_logical_exp(token_value)

            if value is not True and value is not False:
                self.error("Token value is not of boolean data type")

            for identifier in var_identifiers:
                if (ValuesTable.get_var(identifier[0]))[1] == 'bool':
                    val = (value, "bool")
                    ValuesTable.add_var(identifier[0], val)
                else:
                    self.error("Receiving variable is not of BOOL data type")

        elif (ValuesTable.get_var((var_identifiers[0])[0]))[1] == "char":
            if (len(token_value)) == 1:
                self.parse_char_assign(var_identifiers, token_value)

        else:
            value, token = self.parse_arithmetic_exp(token_value)

            for identifier in var_identifiers:
                if (ValuesTable.get_var(identifier[0]))[1] == "integer":
                    val = (int(value), "integer")
                else:
                    val = (value, "float")
                ValuesTable.add_var(identifier[0], val)

    def parse_char_assign(self, var_identifiers, token_value):
        for identifier in var_identifiers:
            if (ValuesTable.get_var(identifier[0]))[1] == 'char':
                if (token_value[0])[1] == 'char':
                    ValuesTable.add_var(identifier[0], token_value[0])
                else:
                    self.error("Value assigned is not of CHAR data type")
            else:
                self.error("Receiving variable is not of CHAR data type")

    def parse_comparison_exp(self, tokens):
        comparison_stack = []
        expression_stack = []

        tokens.append((')', "rparen"))

        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token[1] == 'lparen':
                self.keep('lparen')
                value, tokens = self.parse_comparison_exp(tokens[i + 1:])
                i = -1

                expression_stack.append(value)

            elif token[1] in VALUES_DATATYPES.difference(set(["identifier"])):
                self.advance()
                if type(token[0]) is str and (token[1] == "integer" or token[1] == "float"):
                    expression_stack.append(float(token[0]))
                    i += 1
                    continue

                expression_stack.append(token[0])

            elif token[1] == 'identifier':
                self.keep('identifier')
                value = ValuesTable.get_var(token[0])
                if value is (int or float):
                    value = float(value)
                expression_stack.append(value)

            elif token[1] in RELATIONAL_TOKENTYPE:
                while len(comparison_stack):
                    operator = comparison_stack.pop()
                    operand_2 = expression_stack.pop()
                    operand_1 = expression_stack.pop()

                    value = comparison_mapping[operator](operand_1, operand_2)
                    expression_stack.append(value)

                self.advance()
                comparison_stack.append(token[0])

            elif token[1] in LOGICAL_TOKENTYPE.union(set(['rparen'])):
                if (self.current_token[1] == 'rparen') and ((i + 1) < len(tokens)):
                    self.keep('rparen')

                while len(comparison_stack):
                    operator = comparison_stack.pop()
                    operand_2 = expression_stack.pop()
                    operand_1 = expression_stack.pop()

                    value = comparison_mapping[operator](operand_1, operand_2)
                    expression_stack.append(value)

                return expression_stack[-1], tokens[i + 1:-1]

            i += 1

    def parse_logical_exp(self, tokens):
        expression_stack = []
        logical_stack = []

        tokens.append((')', "rparen"))
        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token[1] == "lparen":
                self.keep('lparen')
                value, tokens = self.parse_logical_exp(tokens[i + 1:])
                i = -1

                expression_stack.append(value)

            elif token[1] in VALUES_DATATYPES:
                index = self.get_logical_index(i, tokens)
                value, temp_tokens = self.parse_comparison_exp(tokens[i: index])
                tokens = tokens[index:]
                i = -1
                if value == "TRUE":
                    value = True
                elif value == "FALSE":
                    value = False

                expression_stack.append(value)

            elif token[1] in LOGICAL_TOKENTYPE:
                while len(logical_stack) and logic_precedence[token[0]] <= logic_precedence[logical_stack[-1]]:
                    operator = logical_stack.pop()
                    if operator == "NOT":
                        operand_1 = expression_stack.pop()
                        value = logical_mapping[operator](operand_1)
                    else:
                        operand_2 = expression_stack.pop()
                        operand_1 = expression_stack.pop()
                        value = logical_mapping[operator](operand_1, operand_2)

                    expression_stack.append(value)

                self.advance()
                logical_stack.append(token[0])

            elif token[1] == 'rparen':
                if (self.current_token[1] == 'rparen') and ((i + 1) < len(tokens)):
                    self.keep('rparen')

                while len(logical_stack):
                    operator = logical_stack.pop()
                    if operator == "NOT":
                        operand_1 = expression_stack.pop()
                        value = logical_mapping[operator](operand_1)
                    else:
                        operand_2 = expression_stack.pop()
                        operand_1 = expression_stack.pop()
                        value = logical_mapping[operator](operand_1, operand_2)
                    expression_stack.append(value)

                return expression_stack[-1], tokens[i + 1:-1]

            i += 1

    def parse_arithmetic_exp(self, tokens):  # computes arithmetic expressions with precedence rules
        operator_stack = []
        expression_stack = []

        tokens.append((')', "rparen"))

        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token[1] == "lparen":
                self.keep('lparen')
                value, tokens = self.parse_arithmetic_exp(tokens[i + 1:])
                i = -1

                expression_stack.append(value)

            elif token[1] == "integer" or token[1] == "float":
                self.advance()
                expression_stack.append(float(token[0]))

            elif token[1] == "operators":
                while len(operator_stack) and precedence[token[0]] <= precedence[operator_stack[-1]]:
                    operator = operator_stack.pop()
                    operand_2 = expression_stack.pop()
                    operand_1 = expression_stack.pop()

                    value = operator_mapping[operator](operand_1, operand_2)
                    expression_stack.append(value)

                self.keep('operators')
                operator_stack.append(token[0])

            elif token[1] == "rparen":
                if self.current_token[1] == 'rparen':
                    self.keep('rparen')

                while len(operator_stack):
                    operator = operator_stack.pop()
                    operand_2 = expression_stack.pop()
                    operand_1 = expression_stack.pop()

                    value = operator_mapping[operator](operand_1, operand_2)
                    expression_stack.append(value)

                return expression_stack[-1], tokens[i + 1:-1]

            i += 1

    # get the last index of a single assignment statement
    def assign_limit(self):
        pos = self.assignment_index()

        while (self.tokens[pos])[1] == 'lparen':
            pos += 1

        if (self.tokens[pos])[1] in VALUES_DATATYPES:
            pos += 1

        while (self.tokens[pos])[1] in (RELATIONAL_TOKENTYPE.union(set(['operators']), LOGICAL_TOKENTYPE)):
            pos += 1
            if (self.tokens[pos])[1] in VALUES_DATATYPES:
                pos += 1

            # if current token is left parenthesis:
            while (self.tokens[pos])[1] == 'lparen':
                pos += 1
                if (self.tokens[pos])[1] in VALUES_DATATYPES:
                    pos += 1

            # if current token is right parenthesis:
            while (self.tokens[pos])[1] == 'rparen':
                pos += 1

            if (self.tokens[pos])[1] == 'assignment':
                pos -= 1

        return pos

    def assignment_index(self):
        pos = self.pos
        pos += 1
        while (self.tokens[pos])[1] == 'assignment':
            pos += 1
            if (self.tokens[pos])[1] == 'identifier':
                pos += 1
            if (self.tokens[pos])[1] in (
                    RELATIONAL_TOKENTYPE.union(set(['identifier', 'operators']), RESERVED_KEYWORDS)) \
                    and (self.tokens[pos - 1])[1] != 'assignment':
                pos -= 1

        return pos

    # get index of logical operators
    def get_logical_index(self, i, tokens):
        pos = i
        while pos < len(tokens):
            token = tokens[pos]
            if token[1] in LOGICAL_TOKENTYPE.union(set(['rparen'])):
                break;
            pos += 1

        if pos > len(tokens):
            self.error("Index value is greater than list length")

        return pos

    def get_stop_index(self):
        pos = self.pos  # START
        start_stack = [pos]

        while len(start_stack):
            pos += 1

            if (self.tokens[pos])[1] == 'START':
                start_stack.append(pos)
            if (self.tokens[pos])[1] == 'STOP':
                start_stack.pop()
                stop_index = pos

        return stop_index

    def get_values(self, expression):
        index = 0
        size = len(expression)
        token_value = []

        while index < size:
            token = expression[index]

            if token[1] == "identifier" and ValuesTable.check_var(token[0]):
                token_value.append(ValuesTable.get_var(token[0]))

            else:
                if token[1] == "bool":
                    token = (token[0].replace("\"", ""), "bool")

                # checking for UNARY OPERATORS
                if token[1] == 'operators':
                    if (len(expression) > 2 and ((expression[index - 1])[1] == 'operators' or
                                                 (expression[index - 1]) == (expression[size - 1]))) \
                            or (len(expression) == 2 and index == 0):
                        if token[0] == '-':
                            temp = expression[index + 1]
                            temp_val = ValuesTable.get_var(temp[0])
                            token = ((float(temp_val[0]) * -1), temp_val[1])
                            index += 1
                            self.advance()

                token_value.append(token)

            index += 1

        return token_value
