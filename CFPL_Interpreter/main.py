from parse_tokens import *
from var_table import ValuesTable

text = open('text.txt', 'r').read()
# print(text)
tokens = tokenizer(text)
# print(tokens)
output = Parser(tokens)
output.parse_program()


# print(output.parse_declarations_block())
