import re
from Constants import *

class LexAnalyzer:
    status = 0

    def __init__(self):
        status = 0

    def parse(self, statement):
        statement = self.replacecharstatement(statement)
        tokens = []
        tokens = statement.split(" ")
        arrforlex = []
        actualvalue = []
        ctr = 0

        for token in tokens:
            ctr = ctr + 1
            type = 0
            if token == '':
                continue
            else:
                type = self.checktoken(token)
            if type == Constants.CONST_ERROR:
                arrforlex.clear()
                arrforlex.insert(0, Constants.CONST_ERROR)
                arrforlex.insert(1, 'Unexpected token: ' + token)
                break
            else:
                arrforlex.insert(ctr, type)
            actualvalue.insert(ctr, token)
        return arrforlex, actualvalue

    def checktoken(self, token):
        if (re.match(r'^VAR [a-zA-Z_$][a-zA-Z_$0-9]*$', token)):
            type = Constants.CONST_VAR
        if (re.match(r'^OUTPUT:\s*', token)):
            type = Constants.CONST_OUTPUT
        elif (re.match(r'((-*)\d+\.\d+)', token)):  # float values
            type = Constants.CONST_FLOAT
        elif (re.match(r'((-*)\d+)', token)):  # integer values
            type = Constants.CONST_INT
        elif (re.match(r'(^[a-zA-Z_$][a-zA-Z_$0-9]*$)', token)):
            type = self.parseAlpha(token)
        elif (re.match(r'(^\"\#\"$)', token)):  # special characters
            type = Constants.CONST_NEXTLINE
        elif (re.match(r'(^\"\[(.)\]\"$)', token)):  # special characters
            type = Constants.CONST_SPECIALCHAROUT
        elif (re.match(r'(\'\s*(.+)\')', token)):  # String in Single Quote
            type = Constants.CONST_STRING_S
        elif (re.match(r'(\"(.+)\")', token)):  # String in Double Quote
            type = Constants.CONST_STRING_D
            type = self.parseAlpha(token, type)
        elif (re.match(r'.', token)):  # special characters
            type = self.parseSpecialChar(token)
        else:
            type = Constants.CONST_ERROR
        return type

    def parseAlpha(self, token, default = Constants.CONST_VARIABLE):
        type = default
        # print(token)
        if token == 'VAR':
            type = Constants.CONST_VAR
        elif token == 'AS':
            type = Constants.CONST_AS
        elif token == 'INT':
            type = Constants.CONST_TYPE_INT
        elif token == 'CHAR':
            type = Constants.CONST_TYPE_CHAR
        elif token == 'FLOAT':
            type = Constants.CONST_TYPE_FLOAT
        elif token == 'BOOL':
            type = Constants.CONST_TYPE_BOOL
        elif token == 'START':
            type = Constants.CONST_START
        elif token == 'STOP':
            type = Constants.CONST_STOP
        elif token == 'OUTPUT:':
            type = Constants.CONST_OUTPUT
        elif token == 'AND':
            type = Constants.CONST_AND
        elif token == 'OR':
            type = Constants.CONST_OR
        elif token == 'NOT':
            type = Constants.CONST_NOT
        elif token == '\"TRUE\"':
            type = Constants.CONST_BOOL_TRUE
        elif token == '\"FALSE\"':
            type = Constants.CONST_BOOL_FALSE
        return type

    def parseSpecialChar(self, token):
        type = Constants.CONST_SPECIAL
        if token == '=':
            type = Constants.CONST_EQ
        elif token == '(':
            type = Constants.CONST_OPEN_PAREN
        elif token == ')':
            type = Constants.CONST_CLOSE_PAREN
        elif token == '+':
            type = Constants.CONST_OP_PLUS
        elif token == '-':
            type = Constants.CONST_OP_MINUS
        elif token == '*':
            type = Constants.CONST_ASTERISK 
        elif token == '/':
            type = Constants.CONST_OP_DIV
        elif token == ',':
            type = Constants.CONST_COMMA
        elif token == '#':
            type = Constants.CONST_ERROR
        elif token == '[':
            type = Constants.CONST_OPEN_BRAC
        elif token == ']':
            type = Constants.CONST_CLOSE_BRAC
        elif token == '&':
            type = Constants.CONST_AMPERSAND
        elif token == '%':
            type = Constants.CONST_PERCENTAGE
        elif token == '<':
            type = Constants.CONST_LESS_THAN
        elif token == '>':
            type = Constants.CONST_GREATER_THAN
        elif token == '>=':
           type = Constants.CONST_LOGIC_GREATERTHANEQ
        elif token == '<=':
           type = Constants.CONST_LOGIC_LESSTHANEQ
        elif token == '==':
            type = Constants.CONST_LOGIC_EQUAL
        elif token == '<>':
            type = Constants.CONST_LOGIC_NOTEQUAL
        else:
            type = Constants.CONST_ERROR
        return type

    def replacecharstatement(self, statement):
        statement = statement.replace(",", " , ")
        statement = statement.replace("+", " + ")
        statement = statement.replace("*", " * ")
        statement = statement.replace("/", " / ")
        statement = statement.replace("=", " = ")
        statement = statement.replace("(", " ( ")
        statement = statement.replace(")", " ) ")
        statement = statement.replace("= =", "==")
        statement = statement.replace("< =", "<=")
        statement = statement.replace("> =", ">=")
        statement = statement.replace("<>", " <> ")
        statement = statement.replace("==", " == ")
        return statement
