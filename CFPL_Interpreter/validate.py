class Validate: # validates tokens using DFA
    def __init__(self):
        self.flag = True

    def is_valid_syntax(self, tokens):
        state = 0

        table = [
            [1, 6, 6, 6, 6],
            [6, 2, 6, 6, 6],
            [6, 6, 3, 4, 6],
            [6, 2, 6, 6, 6],
            [6, 6, 6, 6, 5],
            [6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6]
        ]

        for token in tokens:

            if token[0] == "VAR":
                input_type = 0
                state = table[state][input_type]
                if state == 6:
                    break

            elif token[1] == "identifier":
                input_type = 1
                state = table[state][input_type]
                if state == 6:
                    break

            elif token[0] == ",":
                input_type = 2
                state = table[state][input_type]
                if state == 6:
                    break

            elif token[0] == "AS":
                input_type = 3
                state = table[state][input_type]
                if state == 6:
                    break

            elif token[1] == "data_types":
                input_type = 4
                state = table[state][input_type]
                if state == 6:
                    break

        if state != 5:
            self.flag = False

        return self.flag
