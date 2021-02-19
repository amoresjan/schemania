from _ast import Expression

from Constants import *
from OutputExpression import *
from LexAnalyzer import *

class Interpreter:

    variables = {}
    started = False
    ended = False

    def __init__(self):
        self.status = True

    def execute(self, lines):
        linectr = 0
        p = LexAnalyzer()
        for str in lines:
            linectr += 1
            str = str.rstrip("\n")
            if len(str.strip()) == 0:
                continue
            lexArray = actual = []
            lexArray, actual = p.parse(str)
            if lexArray[0] == Constants.CONST_ERROR:
                lexArray[1] = lexArray[1] + ' at line %d ' % linectr
                print(lexArray[1] )
                self.status = False
                break
            self.run(lexArray, actual)
            if (not self.status):
                print("Not complete")
                break
        if self.status and self.started and (not self.ended): print("Not complete")
        else: print("Complete")

    def run(self, tokens, actual):
        statementtype = tokens[0]
        if statementtype == Constants.CONST_VAR:
            self.status = True
           
        elif statementtype == Constants.CONST_START:
            if len(tokens) == 1 and not self.started and not self.ended:
                self.started = True
            else:
                self.status = False
        elif statementtype == Constants.CONST_STOP:
            self.ended = True
            if len(tokens) == 1 and self.started:
                self.ended = True
            else:
                self.status = False
                
        elif statementtype == Constants.CONST_ASTERISK: #comment
            return
        elif statementtype == Constants.CONST_OUTPUT:
            if self.started:
                if (len(tokens) > 1):
                    self.status = True
                else:
                   self.status = Constants.CONST_ERROR
            else:
                self.status = False
        elif statementtype == Constants.CONST_VARIABLE:
            self.status = True
        else:
            self.status = False
        return self.status

    
