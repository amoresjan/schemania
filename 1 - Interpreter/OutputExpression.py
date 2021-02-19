
from Constants import *
import re
import sys

class OutputExpression:
    output_states = [[	0	,	0	,	0	,	0	],
                    [	1	,	2	,	0	,	0	],
                    [	0	,	0	,	1	,	0	],
                    [	0	,	0	,	0	,	0	]]


    def __init__(self):
        state = 0

    def checksyntax(self, tokens ):
        state = 1  # starting state
        for token in tokens:
            prev = state
            curr = self.getCode(token)
            state = self.output_states[state][curr]
        if state == 2:
            return True
        else:
            return False

    def getCode(self, token):
        if token == Constants.CONST_OUTPUT:
            return 0
        elif (token == Constants.CONST_VARIABLE or
              token == Constants.CONST_STRING_D or
              token == Constants.CONST_STRING_S or
              token == Constants.CONST_NEXTLINE or
              token == Constants.CONST_SPECIALCHAROUT):
            return 1
        elif token == Constants.CONST_AMPERSAND:
            return 2
        else:
            return 3

    def print(self, tokens, actual, vars):
        str = ''
        ctr = 0
        for token in tokens:
            if token == Constants.CONST_VARIABLE:
                variable = vars.get(actual[ctr], None )
                if variable != None:
                    if (list(variable)[1] == Constants.CONST_TYPE_CHAR):
                        str = str + re.sub('\'', '', list(variable)[0])
                    else:
                        str = str + repr(list(variable)[0])
                else:
                    print(colored("Unknown variable ", actual[ctr], 'red'))
                    break
            elif token == Constants.CONST_STRING_D:
                line = re.sub('\"', '', actual[ctr])
                str = str + line
            elif (token == Constants.CONST_STRING_S or
                  token == Constants.CONST_TYPE_CHAR):
                line = re.sub('\'', '', actual[ctr])
                str = str + line
            elif token == Constants.CONST_NEXTLINE:
                str = str + "\n"
            elif token == Constants.CONST_SPECIALCHAROUT:
                str = str + actual[ctr][2:3]
            else:
                ctr += 1
                continue
            ctr += 1
        print(str)