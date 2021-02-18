from tokenizer import *
from parse_tokens import *

text = open('text.txt', 'r').read()
# print(text)
tokens = tokenizer(text)
output = Parser(tokens)
print(output.parse_declarations_block())

# while True:
# lines = input(">> ")

# output = Parser(tokens)
# print(output.parse_declaration())

# for token in tokens:
#     if token[1] == "identifier":
#         print("Variable = ", token[0])
