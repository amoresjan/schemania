from Interpreter import Interpreter

f = open('Run.txt', "r")
lines = f.readlines()
f.close()
i = Interpreter()
i.execute(lines)