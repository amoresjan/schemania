from parse_tokens import *
from var_table import ValuesTable

text = open('text.txt', 'r').read()
tokens = tokenizer(text)
# print(tokens)
output = Parser(tokens)
output.parse_program()
# print(ValuesTable.val)

